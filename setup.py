#!/usr/bin/env python
import os
import sys
import re

# require python 3.8 or newer
if sys.version_info < (3, 9):
    print("Error: dbt does not support this version of Python.")
    print("Please upgrade to Python 3.9 or higher.")
    sys.exit(1)

# require version of setuptools that supports find_namespace_packages
from setuptools import setup

try:
    from setuptools import find_namespace_packages
except ImportError:
    # the user has a downlevel version of setuptools.
    print("Error: dbt requires setuptools v40.1.0 or higher.")
    print('Please upgrade setuptools with "pip install --upgrade setuptools" ' "and try again")
    sys.exit(1)

# pull long description from README
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), "r", encoding="utf8") as f:
    long_description = f.read()


# get this package's version from dbt/adapters/<name>/__version__.py
def _get_plugin_version_dict():
    _version_path = os.path.join(this_directory, "dbt", "adapters", "spark", "__version__.py")
    _semver = r"""(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"""
    _pre = r"""((?P<prekind>a|b|rc)(?P<pre>\d+))?"""
    _build = r"""(\+build[0-9]+)?"""
    _version_pattern = rf"""version\s*=\s*["']{_semver}{_pre}{_build}["']"""
    with open(_version_path) as f:
        match = re.search(_version_pattern, f.read().strip())
        if match is None:
            raise ValueError(f"invalid version at {_version_path}")
        return match.groupdict()


package_name = "dbt-spark"
package_version = "1.9.1"
description = """The Apache Spark adapter plugin for dbt"""

odbc_extras = ["pyodbc~=5.1.0"]
pyhive_extras = [
    "PyHive[hive_pure_sasl] @ git+https://github.com/glydways/PyHive@v0.7.2#egg=PyHive",
    "thrift>=0.11.0,<0.17.0",
]
session_extras = ["pyspark>=3.0.0,<4.0.0"]
all_extras = odbc_extras + pyhive_extras + session_extras

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="dbt Labs",
    author_email="info@dbtlabs.com",
    url="https://github.com/dbt-labs/dbt-spark",
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    include_package_data=True,
    install_requires=[
        "sqlparams>=3.0.0",
        "dbt-common>=1.10,<2.0",
        "dbt-adapters>=1.7,<2.0",
        # add dbt-core to ensure backwards compatibility of installation, this is not a functional dependency
        "dbt-core>=1.8.0",
    ],
    extras_require={
        "ODBC": odbc_extras,
        "PyHive": pyhive_extras,
        "session": session_extras,
        "all": all_extras,
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
)
