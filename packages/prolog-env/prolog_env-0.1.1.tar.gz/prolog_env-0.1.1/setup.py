# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='prolog-env',
    version="v0.1.1",
    description='A Python package providing an environment for AI agents to test their Prolog code.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Yuan XU',
    author_email='dev.source@outlook.com',
    url='https://github.com/NewJerseyStyle/prolog-env',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['gymnasium', 'janus-swi'],
    extras_require={
        'toolbox': ['transformers'],
    },
)