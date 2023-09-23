
from setuptools import setup, find_packages
from pkg_resources import parse_requirements
from os import path
from io import open
import codecs
import re
import os

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
with open('requirements.txt') as requirements_file:
    install_requires = [str(requirement) for requirement in parse_requirements(requirements_file)]

setup(
    name='autonomy',
    version='0.0.1',
    description='autonomy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/autonomy/autonomy',
    author='',
    packages=find_packages(),
    include_package_data=True,
    author_email='',
    license='FREEDOM',
    install_requires=install_requires,
    scripts=['bin/a'],
    classifiers=[
        'Whadup',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
    ], python_requires='>=3.7')
