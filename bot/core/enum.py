from enum import StrEnum


class UserStatus(StrEnum):
    common: str = "common"
    premium: str = "premium"

class ProjectStatus(StrEnum):
    common: str = "COMMON"
    premium: str = "PREMIUM"