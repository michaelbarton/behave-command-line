import pathlib
import typing

import setuptools


def read_requirements(name: str) -> typing.List[str]:
    """Read requirements from a file in requirements directory."""
    return pathlib.Path("requirements/{}.txt".format(name)).read_text().splitlines()


setuptools.setup(
    install_requires=read_requirements("default"), tests_require=read_requirements("dev")
)
