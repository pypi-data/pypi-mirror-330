import os
import pathlib

from setuptools import setup

from pkg_resources import parse_requirements

# ───────────────────────────────────────────────────────────────────────────────────────────── #
# ─── Utils
# ───────────────────────────────────────────────────────────────────────────────────────────── #


def get_requirements(file: pathlib.Path):
    """Reads package dependencies and returns a list of
    requirement. e.g. ['django==1.6.2', 'mezzanine==1.6.2']"""
    file_path = os.path.join(here, file)
    with open(str(file_path), encoding="utf-8") as file_object:
        return [str(r) for r in parse_requirements(file_object)]


# ───────────────────────────────────────────────────────────────────────────────────────────── #
# ─── Definitions
# ───────────────────────────────────────────────────────────────────────────────────────────── #
here = pathlib.Path(__file__).parent.resolve()
SETUP_NAME = "turintech_evoml_rocket_client"

with open(f"{here}/.version", "r", encoding="utf-8") as version_file:
    version = version_file.read().strip()

if not version:
    raise ValueError("No version specified. Please specify in .version file.")

setup_path = pathlib.Path(__file__).resolve().parent.parent.parent / "setup"

SETUP_AUTHOR = "Turing Intelligence Technology"
SETUP_AUTHOR_EMAIL = "contact@turintech.ai"

SETUP_DESCRIPTION = "Library with rocket client for the evoML platform."

LICENSE = "TURING INTELLIGENCE TECHNOLOGY LIMITED END-USER LICENCE"

setup_file_requirements = setup_path / "requirements_client.txt"

# ───────────────────────────────────────────────────────────────────────────────────────────── #
# ─── Setup
# ───────────────────────────────────────────────────────────────────────────────────────────── #

setup(
    name=SETUP_NAME,
    version=version,
    packages=[
        "rocket_client",
        "rocket.dtos",
        "rocket.data_types",
        "rocket_rest.tos",
    ],
    py_modules=[
        "rocket_rest.endpoints.router_prefixes",
    ],
    package_dir={"": "src"},
    author=SETUP_AUTHOR,
    author_email=SETUP_AUTHOR_EMAIL,
    license=LICENSE,
    description=SETUP_DESCRIPTION,
    install_requires=get_requirements(file=setup_file_requirements),
)
