"""Negative network vectors are fully offline, not HTTP/DNS integration tests."""
import socket
import unittest
from unittest.mock import patch
from urllib.parse import urlunsplit
from tooling.nexus_n01_a2.network_review import evaluate,redirect_chain

BASE=dict(host='docs.allowed.test',answers=['93.184.216.34'],online=True,verified_grant_fixture=True)
URL='https://docs.allowed.test/article'

class NetworkVectorTest(unittest.TestCase):
    def check(self,url=URL,reason=None,**changes):
        args={**BASE,**changes}
        with patch.object(socket,'getaddrinfo',side_effect=AssertionError('DNS forbidden in review')),patch.object(socket,'create_connection',side_effect=AssertionError('IO forbidden in review')),patch.object(socket,'socket',side_effect=AssertionError('socket forbidden in review')):
            result=evaluate(url,**args)
        self.assertFalse(result.transport_authorized)
        if reason:self.assertEqual(reason,result.reason)
        return result

    def test_positive_exact_host_is_only_fixture_eligible(self):
        self.assertTrue(self.check().eligible_for_test_request)
    def test_offline_is_default(self):
        self.check(reason='OFFLINE',online=False)
    def test_missing_authority_is_refused(self):
        self.check(reason='AUTHORITY_NOT_VERIFIED_FIXTURE',verified_grant_fixture=False)
    def test_string_authority_is_not_verified(self):
        self.check(reason='AUTHORITY_NOT_VERIFIED_FIXTURE',verified_grant_fixture='true')
    def test_stop_revokes_new_admission(self):
        self.check(reason='STOP_REQUESTED',cancelled=True)
    def test_expired_authority_is_refused(self):
        self.check(reason='GRANT_EXPIRED',expired=True)
    def test_proxy_is_not_an_implicit_network_route(self):
        self.check(reason='INDIRECT_NETWORK_UNREVIEWED',proxy_present=True)
    def test_other_domain_is_refused(self):
        self.check('https://elsewhere.test/',reason='HOST_NOT_ALLOWLISTED')
    def test_suffix_trick_is_refused(self):
        self.check('https://docs.allowed.test.evil.test/',reason='HOST_NOT_ALLOWLISTED')
    def test_prefix_trick_is_refused(self):
        self.check('https://evildocs.allowed.test/',reason='HOST_NOT_ALLOWLISTED')
    def test_subdomain_is_denied_by_default(self):
        self.check('https://child.docs.allowed.test/',reason='HOST_NOT_ALLOWLISTED')
    def test_explicit_subdomain_fixture_is_eligible(self):
        self.assertTrue(self.check('https://child.docs.allowed.test/',subdomains=True).eligible_for_test_request)
    def test_subdomain_does_not_allow_parent(self):
        self.check('https://allowed.test/',subdomains=True,reason='HOST_NOT_ALLOWLISTED')
    def test_userinfo_is_refused(self):
        self.check('https://docs.allowed.test@elsewhere.test/',reason='URL_CREDENTIALS')
    def test_password_is_refused(self):
        # Structured synthetic fixture: no credential-shaped URL stored in source.
        url=urlunsplit(('https','fixture-user:fixture-value@docs.allowed.test','/','',''))
        self.check(url,reason='URL_CREDENTIALS')
    def test_plain_http_is_refused(self):
        self.check('http://docs.allowed.test/',reason='UNSUPPORTED_URL')
    def test_file_access_is_not_a_network_source(self):
        self.check('file:///etc/hosts',reason='UNSUPPORTED_URL')
    def test_non_http_schemes_are_refused(self):
        for scheme in ('ftp','data','gopher','javascript'):
            with self.subTest(scheme=scheme):self.check(scheme+'://docs.allowed.test/',reason='UNSUPPORTED_URL')
    def test_nonapproved_port_is_refused(self):
        self.check('https://docs.allowed.test:8443/',reason='PORT_NOT_ALLOWED')
    def test_malformed_port_is_refused(self):
        self.check('https://docs.allowed.test:abc/',reason='INVALID_URL')
    def test_fragment_is_refused(self):
        self.check(URL+'#https://elsewhere.test',reason='UNSUPPORTED_URL')
    def test_controls_and_whitespace_are_refused(self):
        for value in ('\n'+URL,URL+'\r\n',URL+' ',URL+'\x00'):
            with self.subTest(value=repr(value)):self.check(value,reason='INVALID_URL')
    def test_backslash_is_refused(self):
        self.check('https://docs.allowed.test\\@127.0.0.1/',reason='INVALID_URL')
    def test_encoded_host_is_refused(self):
        self.check('https://%64ocs.allowed.test/',reason='INVALID_HOST')
    def test_trailing_dot_is_not_silently_normalized(self):
        self.check('https://docs.allowed.test./',reason='INVALID_HOST')
    def test_unicode_host_requires_separate_review(self):
        self.check('https://dócs.allowed.test/',reason='INVALID_URL')
    def test_literal_public_ip_is_not_a_domain(self):
        self.check('https://93.184.216.34/',reason='INVALID_HOST')
    def test_numeric_and_encoded_ip_variants_are_refused(self):
        for target in ('2130706433','0177.0.0.1','0x7f000001','[::1]','[::ffff:127.0.0.1]'):
            with self.subTest(target=target):self.check('https://'+target+'/',reason='INVALID_HOST')
    def test_special_dns_answers_are_refused(self):
        for ip in ('127.0.0.1','10.0.0.1','172.16.0.1','192.168.1.1','169.254.169.254','100.64.0.1','0.0.0.0','192.0.2.1','224.0.0.1','255.255.255.255','::1','fc00::1','fe80::1','ff02::1','::ffff:8.8.8.8','64:ff9b::808:808','2002:0808:0808::1'):
            with self.subTest(ip=ip):self.check(reason='NON_PUBLIC_OR_INVALID_ADDRESS',answers=[ip])
    def test_mixed_dns_set_is_refused(self):
        self.check(reason='NON_PUBLIC_OR_INVALID_ADDRESS',answers=['93.184.216.34','127.0.0.1'])
    def test_empty_dns_is_not_success(self):
        self.check(reason='NO_VERIFIED_DNS_FIXTURE',answers=[])
    def test_invalid_dns_is_refused(self):
        self.check(reason='NON_PUBLIC_OR_INVALID_ADDRESS',answers=['not-an-ip'])
    def test_non_string_and_scoped_dns_are_refused(self):
        for value in (1572395042,True,None,'2001:4860:4860::8888%eth0'):
            with self.subTest(value=value):self.check(reason='NON_PUBLIC_OR_INVALID_ADDRESS',answers=[value])
    def test_malformed_redirect_chain_is_refused(self):
        self.assertEqual('INVALID_CHAIN',redirect_chain([URL],None).reason)
    def test_dns_rebinding_fixture_is_refused_at_second_hop(self):
        result=redirect_chain([URL,URL+'/next'],[['93.184.216.34'],['127.0.0.1']],host=BASE['host'],online=True,verified_grant_fixture=True)
        self.assertEqual('NON_PUBLIC_OR_INVALID_ADDRESS',result.reason)
    def test_redirect_to_nonapproved_domain_is_refused(self):
        result=redirect_chain([URL,'https://elsewhere.test/'],[['93.184.216.34']]*2,host=BASE['host'],online=True,verified_grant_fixture=True)
        self.assertEqual('HOST_NOT_ALLOWLISTED',result.reason)
    def test_redirect_limit_and_loop_are_bounded(self):
        result=redirect_chain([URL]*5,[['93.184.216.34']]*5,host=BASE['host'],online=True,verified_grant_fixture=True)
        self.assertEqual('REDIRECT_BUDGET',result.reason)
    def test_same_host_redirects_are_only_fixture_eligible(self):
        result=redirect_chain([URL,URL+'/next'],[['93.184.216.34']]*2,host=BASE['host'],online=True,verified_grant_fixture=True)
        self.assertTrue(result.eligible_for_test_request);self.assertFalse(result.transport_authorized)
    def test_missing_policy_and_wildcard_are_refused(self):
        for host in ('','*.allowed.test','localhost','127.0.0.1','a.local'):
            with self.subTest(host=host):self.check(reason='INVALID_POLICY',host=host)
    def test_oversized_url_is_refused(self):
        self.check(URL+'a'*4096,reason='INVALID_URL')
    def test_negative_or_boolean_redirect_counter_is_refused(self):
        for counter in (-1,True,1.0):
            with self.subTest(counter=counter):self.check(reason='REDIRECT_BUDGET',redirect_hops=counter)

if __name__=='__main__':unittest.main()
