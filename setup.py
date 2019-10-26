import pathlib
import setuptools

setuptools.setup(
    install_requires=pathlib.Path('requirements.txt').read_text().splitlines()
)
