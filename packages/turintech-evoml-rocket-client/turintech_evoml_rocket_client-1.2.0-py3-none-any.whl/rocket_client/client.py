"""Implements an HTTP client for Rocket API"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
# Core Source imports
from rocket_client.environment_client import EnvironmentClient
from rocket_client.pipeline_client import PipelineClient

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["RocketClient"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Rocket Client                                                         #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
class RocketClient(EnvironmentClient, PipelineClient):
    """This is a client implementation for Rocket"""
