from enum import Enum


class AccountType(Enum):
    Client = 1
    Vendor = 2
    ClientAndVendor = 3


class AccountStatus(Enum):
    In = 1
    Out = 2