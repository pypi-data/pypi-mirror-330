# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Union
from enum import Enum

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["EnvironmentStatus"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Data types                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class EnvironmentStatus(str, Enum):
    """Environment process status"""

    PENDING = "PENDING"
    IN_PROGRESS = "IN PROGRESS"
    CREATED = "CREATED"
    FAILED = "FAILED"

    def is_status(self, status: Union[str, "EnvironmentStatus"]) -> bool:
        return self is EnvironmentStatus(status)
