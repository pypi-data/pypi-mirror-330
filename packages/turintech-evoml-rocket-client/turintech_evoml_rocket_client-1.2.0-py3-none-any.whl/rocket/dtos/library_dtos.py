# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import List

from pydantic import BaseModel, Field

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["LibraryInfo"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      DTO Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# Same as core_wheels.LibraryInfo !!!
# For now, we cannot import from `core_wheels or core_platform` because this would imply a new dependency on the
# pipeline actor, and because the core libraries have transitive dependencies pinned, it would not be compatible with
# previous versions of core libraries


class LibraryInfo(BaseModel):
    """Specification of a library install information (version, extras)"""

    name: str = Field(..., description="Name of the library")
    version: str = Field(..., description="Version of the library")
    extras: List[str] = Field([], description="Extras required to install this library, e.g. name[extras]==version")

    @property
    def extras_str(self) -> str:
        return ",".join(self.extras)

    @property
    def dependency(self) -> str:
        """Returns the dependency information as: name[extras]==version"""
        extras = ",".join(self.extras)
        if extras:
            extras = f"[{extras}]"
        version = f"=={self.version}" if self.version else ""
        return f"{self.name}{extras}{version}"
