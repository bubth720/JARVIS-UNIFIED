import asyncio
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import socket
import ssl
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from tooling.research_b0 import fence
from tooling.research_b0.contracts import Limits, Plan, Refused
from tooling.research_b0.fixtures import DATA, HOST, SLOW, SyntheticServer, TLSMaterial
from tooling.research_b0.policy import LabPolicy
from tooling.research_b0.store import Ledger
from tooling.research_b0.transport import LabPermit, LabResearch


class TransportTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.tls = TLSMaterial()
        cls.addClassCleanup(cls.tls.close)

    async def asyncSetUp(self):
        self.assertIsNotNone(fence.ACTIVE, 'Use python3 -m tooling.research_b0.offline_runner')
        self.temp = tempfile.TemporaryDirectory(prefix='b0-tests-')
        self.addCleanup(self.temp.cleanup)
        self.fixture = await self.enterAsyncContext(SyntheticServer(self.tls))
        self.clients = []
        self.stores = []
        # Failed TLS handshakes intentionally reset the server-side connection.
        # Keep all other loop errors visible; the client asserts TLS_REFUSED.
        loop=asyncio.get_running_loop()
        def expected_tls_failure(loop,context):
            if (context.get('message') == 'Error on transport creation for incoming connection'
                    and isinstance(context.get('exception'),(ssl.SSLError,ConnectionResetError))):
                return
            loop.default_exception_handler(context)
        loop.set_exception_handler(expected_tls_failure)

    async def asyncTearDown(self):
        for client in self.clients:
            tasks = list(client.tasks)
            if tasks:
                await client.stop()
        for ledger in self.stores:
            ledger.close()

    def client(self, limits=None, policy=None, enabled=True, root=None):
        ledger = Ledger(root or Path(self.temp.name)/str(len(self.stores)), limits or Limits())
        self.stores.append(ledger)
        client = LabResearch(policy or LabPolicy(self.fixture), ledger, enabled=enabled)
        self.clients.append(client)
        return client

    async def get(self, client, path='/ok', plan=None):
        plan = plan or self.fixture.plan(path)
        return await client.start(plan, client.approve(plan))

    async def refused(self, code, client=None, path='/ok', plan=None):
        client = client or self.client()
        with self.assertRaisesRegex(Refused, code):
            await self.get(client, path, plan)
        self.assertEqual([], list((client.ledger.root/'tmp').iterdir()))
        self.assertEqual(0, client.ledger.snapshot()['active'])
        return client

    async def progress(self, client):
        async with asyncio.timeout(2):
            while client.ledger.snapshot()['received'] == 0:
                await asyncio.sleep(.005)

    async def test_allowed_domain_real_https_and_provenance(self):
        c = self.client(); data = await self.get(c)
        self.assertEqual(hashlib.sha256(DATA).hexdigest(), data['sha256'])
        self.assertEqual(len(DATA), data['size_bytes'])
        self.assertEqual('VERIFIED_SYNTHETIC', data['validation'])
        self.assertEqual('SIMULATED', data['date_kind'])
        self.assertEqual(1, len(data['transformations']))
        self.assertEqual(1, c.connection_attempts)
        self.assertEqual(1, c.ledger.document_count())

    async def test_generated_manifest_obeys_proposed_closed_schema(self):
        from scripts.contracts import ContractError,validate
        c=self.client();data=await self.get(c)
        schema=json.loads((Path(__file__).resolve().parents[3]/'docs/research-b0/document.schema.json').read_text())
        self.assertTrue(validate(data,schema))
        for value in [dict(data,core_authorized=True),dict(data,size_bytes=True),dict(data,date_kind='REAL')]:
            with self.subTest(value=list(value)),self.assertRaises(ContractError):validate(value,schema)

    async def test_lab_metadata_cannot_extend_production_contract(self):
        from scripts.contracts import ContractError,validate_contract
        root=Path(__file__).resolve().parents[3]
        schema=json.loads((root/'contracts/v1/request-envelope.schema.json').read_text())
        value=json.loads((root/'contracts/v1/examples/request-envelope.valid.json').read_text())
        self.assertTrue(validate_contract('request-envelope',value,schema))
        value['payload']['research_plan']=dict(source_id='fixture')
        with self.assertRaises(ContractError):validate_contract('request-envelope',value,schema)

    async def test_disabled_by_default(self):
        c = self.client(enabled=False)
        await self.refused('LAB_DISABLED', c)
        self.assertEqual(0, c.connection_attempts)

    async def test_forged_payload_cannot_authorize(self):
        c = self.client(); plan = self.fixture.plan()
        for permit in [None, True, {'approved': True}, LabPermit(plan.key, 0, 999999999999)]:
            with self.subTest(permit=type(permit).__name__), self.assertRaisesRegex(Refused, 'AUTHORITY'):
                c.start(plan, permit)
        self.assertEqual(0, c.connection_attempts)

    async def test_permit_is_bound_to_exact_plan(self):
        c = self.client(); p = self.fixture.plan(); permit = c.approve(p)
        with self.assertRaisesRegex(Refused, 'WRONG_PERMIT'):
            c.start(replace(p, source_id='other'), permit)
        self.assertEqual(0, c.connection_attempts)

    async def test_unknown_domain_refused_before_connection(self):
        c = self.client()
        await self.refused('DESTINATION_REFUSED', c, plan=replace(self.fixture.plan(), url='https://unknown.synthetic.test/ok'))
        self.assertEqual(0, c.connection_attempts)

    async def test_subdomain_refused_before_connection(self):
        c = self.client()
        await self.refused('DESTINATION_REFUSED', c, plan=replace(self.fixture.plan(), url=self.fixture.url().replace(HOST, 'sub.'+HOST)))
        self.assertEqual(0, c.connection_attempts)

    async def test_ip_literals_and_internal_addresses_refused(self):
        c = self.client()
        for host in ['127.0.0.1','10.0.0.1','169.254.169.254','2130706433','0177.0.0.1','[::1]','[::ffff:127.0.0.1]']:
            with self.subTest(host=host):
                await self.refused('DESTINATION_REFUSED', c, plan=replace(self.fixture.plan(), url=f'https://{host}:{self.fixture.port}/ok'))
        self.assertEqual(0, c.connection_attempts)

    async def test_malformed_urls_and_forbidden_schemes_refused(self):
        c = self.client()
        for url in ['file:///tmp/document','ftp://lab.synthetic.test/ok','http://lab.synthetic.test/ok',
                    self.fixture.url()+'?next=external',self.fixture.url()+'#fragment',
                    self.fixture.url().replace(HOST, HOST+'.'),self.fixture.url().replace(HOST,'lab%2esynthetic.test'),
                    self.fixture.url().replace('/ok','/../ok'),self.fixture.url()+'\r\nInjected: value',
                    self.fixture.url().replace(HOST,'u:p@'+HOST), 'https://[invalid/ok',
                    self.fixture.url().replace(HOST, HOST+'\\@other.test')]:
            with self.subTest(url=url), self.assertRaises(Refused):
                c.approve(replace(self.fixture.plan(), url=url))
        self.assertEqual(0, c.connection_attempts)

    async def test_other_loopback_port_refused(self):
        c = self.client(); p = replace(self.fixture.plan(), url=f'https://{HOST}:1/ok')
        await self.refused('DESTINATION_REFUSED', c, plan=p)
        self.assertEqual(0, c.connection_attempts)

    async def test_suspicious_mixed_dns_answers_refused(self):
        async def resolver(host):return ('127.0.0.1','10.0.0.1')
        c = self.client(policy=LabPolicy(self.fixture, resolver=resolver))
        await self.refused('DNS_DESTINATION_CHANGED', c)
        self.assertEqual(0, c.connection_attempts)

    async def test_dns_rebinding_before_connection_refused(self):
        answers = iter([('127.0.0.1',), ('203.0.113.1',)])
        async def resolver(host):return next(answers)
        c = self.client(policy=LabPolicy(self.fixture, resolver=resolver))
        await self.refused('DNS_DESTINATION_CHANGED', c)
        self.assertEqual(0, c.connection_attempts)

    async def test_connection_uses_pinned_ip_without_further_dns(self):
        calls=[]
        async def resolver(host):
            calls.append(host)
            return ('127.0.0.1',) if len(calls)<=2 else ('10.0.0.1',)
        c=self.client(policy=LabPolicy(self.fixture,resolver=resolver))
        with patch('socket.getaddrinfo',side_effect=AssertionError('Unexpected real DNS')):
            await self.get(c)
        self.assertEqual(2,len(calls))
        self.assertEqual(1,c.connection_attempts)

    async def test_destination_changed_after_approval_refused(self):
        c = self.client(); p = self.fixture.plan(); permit = c.approve(p)
        c.policy.ip = '10.0.0.1'
        with self.assertRaisesRegex(Refused, 'PINNED_ADDRESS_CHANGED'):
            await c.start(p, permit)
        self.assertEqual(0, c.connection_attempts)

    async def test_relative_redirect_allowed_and_traced(self):
        c = self.client(); result = await self.get(c, '/redirect')
        self.assertEqual(self.fixture.url('/redirect'), result['origin_url'])
        self.assertEqual(self.fixture.url('/ok'), result['final_url'])
        self.assertEqual(2, c.connection_attempts)

    async def test_external_redirect_denied_before_second_connection(self):
        c = await self.refused('DESTINATION_REFUSED', path='/external')
        self.assertEqual(1, c.connection_attempts)
        self.assertEqual(['/external'], self.fixture.requests)

    async def test_redirect_to_private_ip_denied(self):
        c = await self.refused('DESTINATION_REFUSED', path='/private')
        self.assertEqual(1, c.connection_attempts)

    async def test_redirect_cycle_refused(self):
        c = await self.refused('REDIRECT_CYCLE', path='/chain')
        self.assertEqual(1, c.connection_attempts)

    async def test_zero_redirect_budget_refused(self):
        await self.refused('REDIRECT_QUOTA', self.client(Limits(redirects=0)), '/redirect')

    async def test_untrusted_ca_refused(self):
        c = self.client(policy=LabPolicy(self.fixture, tls=ssl.create_default_context()))
        await self.refused('TLS_REFUSED', c)
        self.assertEqual([], self.fixture.requests)

    async def test_tls_hostname_is_verified(self):
        wrong = TLSMaterial('wrong.synthetic.test')
        self.addCleanup(wrong.close)
        fixture = await self.enterAsyncContext(SyntheticServer(wrong))
        c = self.client(policy=LabPolicy(fixture))
        await self.refused('TLS_REFUSED', c, plan=fixture.plan())

    async def test_disabling_tls_verification_refused(self):
        ctx = ssl.create_default_context();ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
        with self.assertRaisesRegex(Refused, 'TLS_VERIFICATION_REQUIRED'):
            LabPolicy(self.fixture, tls=ctx)

    async def test_http_error_and_incomplete_and_interrupt(self):
        for path, code in [('/error','HTTP_503'),('/incomplete','TRUNCATED_RESPONSE'),('/disconnect','TRUNCATED_RESPONSE')]:
            with self.subTest(path=path):await self.refused(code, path=path)

    async def test_document_size_quota(self):
        c = await self.refused('DOCUMENT_QUOTA', self.client(Limits(document_bytes=16)))
        self.assertEqual(0, c.ledger.snapshot()['received'])

    async def test_announced_excessive_volume_refused_without_body(self):
        c = await self.refused('DOCUMENT_QUOTA', path='/huge')
        self.assertEqual(0, c.ledger.snapshot()['received'])

    async def test_cumulative_mission_bytes_enforced_in_stream(self):
        c = await self.refused('MISSION_BYTES', self.client(Limits(mission_bytes=100)), '/stream')
        self.assertEqual(101, c.ledger.snapshot()['received'])
        self.assertEqual(0, c.ledger.document_count())

    async def test_temporary_storage_quota_enforced_and_released(self):
        c = await self.refused('TEMPORARY_QUOTA', self.client(Limits(temporary_bytes=100)), '/stream')
        self.assertEqual(0, c.ledger.snapshot()['temporary'])

    async def test_timeout_closes_and_cleans(self):
        await self.refused('TIMEOUT', self.client(Limits(timeout_seconds=.12)), '/stall')

    async def test_uncontrolled_persistent_connection_times_out(self):
        c = await self.refused('TIMEOUT', self.client(Limits(timeout_seconds=.12)), '/persistent')
        self.assertEqual(0, c.ledger.document_count())

    async def test_extra_body_is_refused(self):
        await self.refused('EXCESS_BODY', path='/extra')

    async def test_chunked_compressed_and_oversized_headers_refused(self):
        for path, code in [('/encoding','ENCODING_REFUSED'),('/chunked','ENCODING_REFUSED'),('/huge-header','HEADER')]:
            with self.subTest(path=path):await self.refused(code, path=path)

    async def test_corrupted_file_is_not_published(self):
        c = await self.refused('HASH_MISMATCH', path='/corrupt')
        self.assertEqual([], list((c.ledger.root/'objects').iterdir()))

    async def test_invalid_text_rejected(self):
        await self.refused('INVALID_TEXT', path='/invalid-text')

    async def test_cancel_during_real_transfer_and_clean(self):
        c = self.client();p = self.fixture.plan('/slow');task = c.start(p,c.approve(p))
        await self.progress(c);await c.stop()
        self.assertTrue(task.cancelled())
        self.assertEqual('CANCELLED', c.ledger.snapshot()['state'])
        self.assertEqual(0,c.ledger.snapshot()['temporary'])
        self.assertEqual(0,c.ledger.document_count())
        self.assertEqual([],list((c.ledger.root/'tmp').iterdir()))

    async def test_stop_after_commit_never_claims_rollback(self):
        c=self.client();p=self.fixture.plan();result=await self.get(c,plan=p)
        stopped=await c.stop()
        self.assertEqual(dict(state='COMPLETED',stop_observed=True,documents_preserved=1),stopped)
        self.assertEqual(result,c.ledger.cached(p))

    async def test_full_audit_quota_cannot_block_cancellation(self):
        c=self.client(Limits(events=2));p=self.fixture.plan('/slow');task=c.start(p,c.approve(p))
        await self.progress(c);stopped=await c.stop()
        self.assertTrue(task.cancelled())
        self.assertEqual('CANCELLED',stopped['state'])
        self.assertTrue(stopped['stop_observed'])
        self.assertEqual(0,c.ledger.snapshot()['active'])
        with c.ledger.connection() as db:self.assertEqual(2,db.execute('SELECT count(*) FROM events').fetchone()[0])

    async def test_pause_reopen_resume_preserves_budgets_without_duplicates(self):
        root=Path(self.temp.name)/'resume';c=self.client(root=root);p=self.fixture.plan('/slow')
        old=c.approve(p);task=c.start(p,old);await self.progress(c);await c.stop(pause=True)
        self.assertTrue(task.cancelled());before=c.ledger.snapshot();c.ledger.close()
        second=self.client(root=root)
        with self.assertRaisesRegex(Refused,'AUTHORITY'):
            second.start(p,old)
        result=await self.get(second,plan=p)
        self.assertEqual(2,second.ledger.snapshot()['requests'])
        self.assertEqual(before['received']+len(SLOW),second.ledger.snapshot()['received'])
        counters=second.ledger.snapshot();again=await self.get(second,plan=p)
        self.assertEqual(result,again)
        self.assertEqual(counters['requests'],second.ledger.snapshot()['requests'])
        self.assertEqual(1,second.ledger.document_count())
        self.assertEqual(1,len(list((root/'objects').iterdir())))

    async def test_owner_lock_prevents_concurrent_recovery(self):
        c=self.client()
        with self.assertRaisesRegex(Refused,'STORE_OWNER_ACTIVE'):Ledger(c.ledger.root,Limits())

    async def test_recovery_cleans_owned_crash_partial_only(self):
        c=self.client();root=c.ledger.root
        (root/'tmp'/('a'*32+'.part')).write_bytes(b'partial synthetic')
        c.ledger.state('RUNNING');c.ledger.close()
        second=self.client(root=root)
        self.assertEqual('INTERRUPTED',second.ledger.snapshot()['state'])
        self.assertEqual([],list((root/'tmp').iterdir()))

    async def test_resume_cannot_increase_limits(self):
        c=self.client();root=c.ledger.root;c.ledger.close()
        with self.assertRaisesRegex(Refused,'RESUME_LIMITS_CHANGED'):Ledger(root,Limits(requests=99))

    async def test_connections_over_quota_refused_before_second_connect(self):
        c=self.client();p=self.fixture.plan('/slow');task=c.start(p,c.approve(p));await self.progress(c)
        with self.assertRaisesRegex(Refused,'CONNECTION_QUOTA'):
            await self.get(c,plan=replace(p,source_id='second'))
        self.assertEqual(1,c.ledger.snapshot()['active'])
        self.assertEqual(1,c.connection_attempts)
        await c.stop();self.assertTrue(task.cancelled())
        self.assertEqual([],list((c.ledger.root/'tmp').iterdir()))

    async def test_permit_cannot_be_reused(self):
        c=self.client();p=self.fixture.plan();permit=c.approve(p)
        await c.start(p,permit)
        with self.assertRaisesRegex(Refused,'PERMIT_ALREADY_USED'):await c.start(p,permit)
        self.assertEqual(1,c.connection_attempts)

    async def test_mini_pc_two_connections_remain_bounded(self):
        c=self.client(Limits.profile('mini-pc'));p=self.fixture.plan('/slow')
        first=c.start(p,c.approve(p));second_plan=replace(p,source_id='second')
        second=c.start(second_plan,c.approve(second_plan));await self.progress(c)
        self.assertEqual(2,c.ledger.snapshot()['active'])
        with self.assertRaisesRegex(Refused,'CONNECTION_QUOTA'):
            await self.get(c,plan=replace(p,source_id='third'))
        await asyncio.gather(first,second)
        self.assertEqual(2,c.ledger.document_count())
        self.assertEqual(1,len(list((c.ledger.root/'objects').iterdir())))

    async def test_request_budget_survives_error_and_resume(self):
        c=self.client(Limits(requests=1));await self.refused('HTTP_503',c,'/error')
        await self.refused('REQUEST_QUOTA',c)
        self.assertEqual(1,c.connection_attempts)

    async def test_depth_quota_before_connection(self):
        c=self.client();await self.refused('DEPTH_QUOTA',c,plan=self.fixture.plan(depth=3))
        self.assertEqual(0,c.connection_attempts)

    async def test_mission_deadline_before_connection(self):
        c=self.client(Limits(duration_seconds=.02));await asyncio.sleep(.03)
        await self.refused('MISSION_DEADLINE',c)
        self.assertEqual(0,c.connection_attempts)

    async def test_disk_full_cleanup(self):
        c=self.client()
        with patch('tooling.research_b0.transport.os.fsync',side_effect=OSError('synthetic disk full')):
            await self.refused('TRANSPORT_IO',c)
        self.assertEqual(0,c.ledger.document_count())

    async def test_cache_corruption_never_overwrites_original(self):
        c=self.client();result=await self.get(c);blob=c.ledger.root/'objects'/result['sha256'];blob.write_bytes(b'bad')
        await self.refused('CACHE_INTEGRITY',c)
        self.assertEqual(b'bad',blob.read_bytes())
        self.assertEqual(1,c.connection_attempts)

    async def test_cached_provenance_tampering_refused(self):
        c=self.client();p=self.fixture.plan();result=await self.get(c,plan=p);result['source_id']='forged'
        with c.ledger.connection() as db:db.execute('UPDATE documents SET metadata=?',(json.dumps(result),))
        await self.refused('CACHE_INTEGRITY',c,plan=p)

    async def test_changed_tls_context_after_approval_refused(self):
        context=ssl.create_default_context();policy=LabPolicy(self.fixture,tls=context);c=self.client(policy=policy)
        p=self.fixture.plan();permit=c.approve(p);context.check_hostname=False;context.verify_mode=ssl.CERT_NONE
        with self.assertRaisesRegex(Refused,'TLS_VERIFICATION_REQUIRED'):await c.start(p,permit)
        self.assertEqual(0,c.connection_attempts)

    async def test_no_external_internet_or_dns_syscall(self):
        denied=fence.ACTIVE.denied
        with socket.socket() as s, self.assertRaisesRegex(PermissionError,'B0_EGRESS_DENIED'):
            s.connect(('203.0.113.1',443))
        with self.assertRaisesRegex(PermissionError,'B0_DNS_FORBIDDEN'):
            socket.getaddrinfo('outside.synthetic.test',443)
        self.assertEqual(denied+1,fence.ACTIVE.denied)
        c=self.client();await self.get(c)
        self.assertEqual(1,c.connection_attempts)

    async def test_process_crash_recovery_preserves_counters(self):
        root=Path(self.temp.name)/'crash'
        script="""
import os,sys
from pathlib import Path
from tooling.research_b0.contracts import Limits
from tooling.research_b0.store import Ledger
s=Ledger(Path(sys.argv[1]),Limits());s.enter();s.request();s.charge(17)
(s.root/'tmp'/('b'*32+'.part')).write_bytes(b'synthetic partial')
os._exit(23)
"""
        result=subprocess.run([sys.executable,'-c',script,str(root)],capture_output=True,timeout=10)
        self.assertEqual(23,result.returncode,result.stderr)
        c=self.client(root=root)
        self.assertEqual('INTERRUPTED',c.ledger.snapshot()['state'])
        self.assertEqual(17,c.ledger.snapshot()['received'])
        self.assertEqual(1,c.ledger.snapshot()['requests'])
        self.assertEqual(0,c.ledger.snapshot()['temporary'])
        await self.get(c)
        self.assertEqual(17+len(DATA),c.ledger.snapshot()['received'])
        self.assertEqual(2,c.ledger.snapshot()['requests'])
        self.assertEqual(1,c.ledger.document_count())


class ConfigurationTest(unittest.TestCase):
    def test_invalid_limits_fail_closed(self):
        for kwargs in [dict(connections=0),dict(connections=100),dict(requests=True),dict(document_bytes=-1),
                       dict(timeout_seconds=float('nan')),dict(duration_seconds=0),dict(depth=-1),dict(redirects=99)]:
            with self.subTest(kwargs=kwargs),self.assertRaises(Refused):Limits(**kwargs)

    def test_profiles_are_explicit(self):
        self.assertEqual(1,Limits.profile('android').connections)
        self.assertEqual(2,Limits.profile('mini-pc').connections)
        with self.assertRaises(Refused):Limits.profile('automatic')

    def test_expected_hash_and_plan_fields_required(self):
        for kwargs in [dict(sha256=''),dict(source_id='../escape'),dict(depth=True),dict(content_type='text/html')]:
            values=dict(source_id='fixture',url='https://lab.synthetic.test:1/ok',sha256='a'*64);values.update(kwargs)
            with self.subTest(kwargs=kwargs),self.assertRaises(Refused):Plan(**values)

    def test_unowned_store_and_symlinks_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'unowned';root.mkdir();(root/'original.txt').write_text('preserve')
            with self.assertRaisesRegex(Refused,'UNOWNED_STORE'):Ledger(root,Limits())
            link=Path(tmp)/'link';link.symlink_to(root)
            with self.assertRaisesRegex(Refused,'STORE_SYMLINK'):Ledger(link,Limits())
            self.assertEqual('preserve',(root/'original.txt').read_text())
