from dataclasses import dataclass


@dataclass
class StaffInfoDb:
    StaffId: int = -1
    LoginName: str = ''
    EmailAddress: str = ''


@dataclass
class PolicynoEntity:
    PolicyNo: str
    EmailDateCreated: str
