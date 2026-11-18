"""Defense in depth for the *test process*, in addition to transport policy.

The CI additionally runs inside a loopback-only OS network namespace. An audit
hook is not a sandbox for arbitrary hostile Python/native code.
"""
import socket
import sys

ACTIVE = None


class Fence:
    def __init__(self):
        self.ports = set()
        self.accepted = 0
        self.denied = 0
        self.dns_attempts = 0

    def address(self, address):
        if not isinstance(address, tuple) or len(address) != 2 or address[0] != '127.0.0.1' or address[1] not in self.ports:
            self.denied += 1
            raise PermissionError('B0_EGRESS_DENIED')
        self.accepted += 1

    def audit(self, event, args):
        if event == 'socket.getaddrinfo' or event == 'socket.gethostbyname':
            self.dns_attempts += 1
            raise PermissionError('B0_DNS_FORBIDDEN')
        if event == 'socket.connect' and args[0].family in (socket.AF_INET, socket.AF_INET6):
            self.address(args[1])
        if event == 'socket.bind' and args[0].family in (socket.AF_INET, socket.AF_INET6):
            if args[1] != ('127.0.0.1', 0):
                self.denied += 1
                raise PermissionError('B0_BIND_DENIED')


def install():
    global ACTIVE
    if ACTIVE is None:
        ACTIVE = Fence()
        sys.addaudithook(ACTIVE.audit)
    return ACTIVE
