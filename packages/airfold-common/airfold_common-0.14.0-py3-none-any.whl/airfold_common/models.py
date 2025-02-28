from enum import Enum

from airfold_common._pydantic import BaseModel


# Plan models
class CommandType(str, Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    REPLACE = "REPLACE"
    RENAME = "RENAME"
    UNDELETE = "UNDELETE"
    FAIL = "FAIL"
    UPDATE = "UPDATE"

    def __str__(self):
        return self._name_


# Doctor models
class FixStatus(str, Enum):
    FIXED = "fixed"
    FAILED = "failed"

    def __str__(self):
        return self.value


class IssueSeverity(str, Enum):
    WARNING = "warning"
    ERROR = "error"

    def __str__(self):
        return self.value


class Issue(BaseModel, frozen=True):
    id: str
    description: str
    severity: IssueSeverity = IssueSeverity.ERROR


class FixResult(BaseModel, frozen=True):
    issue: Issue
    status: FixStatus
    message: str
