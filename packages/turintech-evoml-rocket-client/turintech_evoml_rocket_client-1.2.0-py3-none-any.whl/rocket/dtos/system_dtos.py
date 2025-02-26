# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from pydantic import Field, BaseModel

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["SystemInfo"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      DTO Models                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class SystemInfo(BaseModel):
    """Information related with the system"""

    rocket_version: str = Field(..., description="Version of the Microservice that generates the pipeline")
    python_version: str = Field(..., description="Python version needed for the EvoML model.")
    ray_version: str = Field(..., description="Ray version used by the microservice,")
    mongoengine_version: str = Field(..., description="Version of the mongoengine installed in the system.")
