# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requirements = (
    'psycopg2',
    'chevron',
    'sqlalchemy>=1.4,<2.0',
    'GeoAlchemy2'
)

dev_requirements = (
    'flake8',
    'pytest',
    'pytest-cov'
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_version(*file_paths):
    """
    see https://github.com/pypa/sampleproject/blob/master/setup.py
    """

    with open(os.path.join(here, *file_paths), 'r') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string. "
                       "Should be at the first line of __init__.py.")


setup(
    name='xplordb',
    version=find_version('xplordb', '__init__.py'),
    description="Python module to read/write data into xplordb database",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/geolandia/openlog/xplordb',
    author='Oslandia',
    author_email='geology@oslandia.com',
    license='AGPLv3',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    test_suite="tests",
    extras_require={
        'dev': dev_requirements
    },
)
