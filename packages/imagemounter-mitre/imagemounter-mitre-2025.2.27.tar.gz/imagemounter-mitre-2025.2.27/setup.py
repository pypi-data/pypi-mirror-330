#!/usr/bin/env python
import os
from setuptools import setup


def get_metadata():
    import re
    with open(os.path.join("imagemounter_mitre", "__init__.py")) as f:
        return dict(re.findall("__([a-z]+)__ = ['\"]([^'\"]+)['\"]", f.read()))

metadata = get_metadata()

try:
    long_description = open("README.rst", "r").read()
except Exception:
    long_description = None

setup(
    name='imagemounter-mitre',
    version=metadata['version'],
    license='MIT',
    packages=['imagemounter_mitre', 'imagemounter_mitre.cli'],
    author='The MITRE Corporation',
    url='https://github.com/mitre/imagemounter',
    description='Command line utility and Python package to ease the (un)mounting of forensic disk images.',
    long_description=long_description,
    entry_points={'console_scripts': ['imount = imagemounter_mitre.cli.imount:main']},
    install_requires=['termcolor>=1.0.0'],
    extras={"magic": ["python-magic>=0.4"]},
    keywords=['encase', 'aff', 'dd', 'disk image', 'ewfmount', 'affuse', 'xmount', 'imount'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Filesystems',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
