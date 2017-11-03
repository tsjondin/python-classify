
from classify import classify, union, typedlist, classifier
from enum import Enum
import ipaddress


@classifier(ipaddress.IPv4Address)
def classify_ipaddress(data, _):
    try:
        return ipaddress.IPv4Address(data)
    except AddressValueError as e:
        raise TypeError('Not a valid IPv4 address')


@classifier(ipaddress.IPv4Network)
def classify_ipnetwork(data, _):
    try:
        return ipaddress.IPv4Address(data)
    except NetmaskValueError as e:
        raise TypeError('Not a valid IPv4 network')


class SNMPv2:
    community = str


class SNMPv3:
    userName = str
    authKey = str
    authProtocol = Enum('AuthProtocol', ('DES'))
    privKey = str
    privProtocol = Enum('PrivProtocol', ('AES'))


class SNMPv3NoAuth:
    userName = str
    privKey = str
    privProtocol = Enum('PrivProtocol', ('AES'))


class SNMPv3NoAuthNoPriv:
    userName = str


class MethodSeedRouterOptions:
    snmp = union(SNMPv2, SNMPv3, SNMPv3NoAuth, SNMPv3NoAuthNoPriv)
    seed_router = ipaddress.IPv4Address


class MethodSubnetOptions:
    snmp = union(SNMPv2, SNMPv3, SNMPv3NoAuth, SNMPv3NoAuthNoPriv)
    subnet = ipaddress.IPv4Network


class MethodIPListOptions:
    snmp = union(SNMPv2, SNMPv3, SNMPv3NoAuth, SNMPv3NoAuthNoPriv)
    ip_list = typedlist(ipaddress.IPv4Address)


class Job:
    name = str
    description = union(str, type(None))
    settings = union(
        MethodSeedRouterOptions,
        MethodSubnetOptions,
        MethodIPListOptions)
    timeout = union(int, type(None))


def test_classes():

    c1 = classify({
        'name': 'my-job',
        'settings': {
            'seed_router': '127.0.0.1',
            'snmp': {
                'community': 'v2c'
            }
        }
    }, Job)
    print(vars(c1))
    print(vars(c1.settings))
