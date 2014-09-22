import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read().strip()

setup(
    name                 = 'behave-command-line',
    version              = read('VERSION'),
    description          = 'Functions for command line cucumber testing with behave',
    author               = 'Michael Barton',
    author_email         = 'mail@michaelbarton.me.uk',
    py_modules           = find_packages(exclude=['tests*']),
    include_package_data = True,
    install_requires     = open('requirements.txt').read().splitlines(),

    classifiers = [
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
