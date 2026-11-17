"""Offline design oracle for N01-B negative vectors.

No DNS resolver, HTTP client, socket, grant verifier or production authorization.
Answers and grant state are synthetic fixture inputs. Even eligible results
always have transport_authorized=False. This must never authorize real IO.
"""
from dataclasses import dataclass
import ipaddress
import re
from urllib.parse import urlsplit

HOST=re.compile(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?\Z')

@dataclass(frozen=True)
class Review:
    eligible_for_test_request: bool
    reason: str
    transport_authorized: bool = False

def canonical_host(value):
    if type(value) is not str or not value.isascii() or len(value)>253:
        return None
    host=value.lower()
    if not HOST.fullmatch(host) or host.endswith(('.localhost','.local')):
        return None
    try:
        ipaddress.ip_address(host)
        return None
    except ValueError:
        return host

def public_answer(value):
    if type(value) is not str or '%' in value:return False
    try:
        ip=ipaddress.ip_address(value)
    except (ValueError,TypeError):
        return False
    if not ip.is_global or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
        return False
    if isinstance(ip,ipaddress.IPv6Address):
        if ip.ipv4_mapped or ip.sixtofour or ip.teredo or ip not in ipaddress.ip_network('2000::/3'):
            return False
    return True

def evaluate(url,*,host,answers=(),subdomains=False,online=False,
             verified_grant_fixture=False,cancelled=False,expired=False,
             proxy_present=False,redirect_hops=0,max_redirects=3):
    """Review a single hop with injected answers; never contacts the named host."""
    deny=lambda code:Review(False,code)
    if online is not True:return deny('OFFLINE')
    if verified_grant_fixture is not True:return deny('AUTHORITY_NOT_VERIFIED_FIXTURE')
    if cancelled is not False:return deny('STOP_REQUESTED')
    if expired is not False:return deny('GRANT_EXPIRED')
    if proxy_present is not False:return deny('INDIRECT_NETWORK_UNREVIEWED')
    if type(max_redirects) is not int or not 0<=max_redirects<=5 or type(redirect_hops) is not int or not 0<=redirect_hops<=max_redirects:
        return deny('REDIRECT_BUDGET')
    allowed=canonical_host(host)
    if allowed is None or type(subdomains) is not bool:return deny('INVALID_POLICY')
    if type(url) is not str or len(url)>4096 or not url.isascii() or '\\' in url or any(ord(c)<=32 or ord(c)==127 for c in url):
        return deny('INVALID_URL')
    try:
        p=urlsplit(url)
        if p.scheme!='https' or not p.netloc or p.fragment:return deny('UNSUPPORTED_URL')
        if p.username is not None or p.password is not None:return deny('URL_CREDENTIALS')
        if p.port not in (None,443):return deny('PORT_NOT_ALLOWED')
        target=canonical_host(p.hostname)
    except ValueError:
        return deny('INVALID_URL')
    if target is None:return deny('INVALID_HOST')
    if target!=allowed and not (subdomains and target.endswith('.'+allowed)):
        return deny('HOST_NOT_ALLOWLISTED')
    if not isinstance(answers,(list,tuple)) or not answers:return deny('NO_VERIFIED_DNS_FIXTURE')
    if len(answers)>16 or not all(public_answer(a) for a in answers):return deny('NON_PUBLIC_OR_INVALID_ADDRESS')
    return Review(True,'ELIGIBLE_FIXTURE_ONLY')

def redirect_chain(urls,answer_sets,**policy):
    if not isinstance(urls,(list,tuple)) or not isinstance(answer_sets,(list,tuple)) or not urls or len(urls)!=len(answer_sets):
        return Review(False,'INVALID_CHAIN')
    for hops,(url,answers) in enumerate(zip(urls,answer_sets)):
        result=evaluate(url,answers=answers,redirect_hops=hops,**policy)
        if not result.eligible_for_test_request:return result
    return result
