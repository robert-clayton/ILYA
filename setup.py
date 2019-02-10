#!/usr/bin/env python
from os import path as op
from setuptools import setup

with open(op.join(op.abspath(op.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().split('\n')

with open('README.md') as f:
    readme = f.read()

with open('VERSION') as f:
    version = f.read()

setup(
    name='label-maker',
    author='Robert Clayton',
    author_email='rclayton@theia.io',
    version=version,
    description='Data preparation bounding box-based machine learning',
    url='https://github.com/robert-clayton/label-maker/',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: GPLv3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='ML labeling image data',
    include_package_data=True,
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown"
)