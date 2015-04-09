from setuptools import setup, find_packages
import behave_command_line

setup(
    name                 = 'behave_command_line',
    version              = behave_command_line.__version__,
    description          = 'Functions for command line cucumber testing with behave',
    author               = 'Michael Barton',
    author_email         = 'mail@michaelbarton.me.uk',
    packages             = ['behave_command_line'],
    install_requires     = open('requirements.txt').read().splitlines(),
    dependency_links     = [
        "https://pypi.fury.io/8w9pcGeJPCmAGrxTL_Ze/michaelbarton/",
        ],

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
