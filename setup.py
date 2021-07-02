#-*- coding: utf-8 -*-

from setuptools import setup
import re, os

version = '2.0.0'

path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

requirements = []
with open(f'{path}/requirements.txt', encoding='UTF8') as f:
  requirements = f.read().splitlines()

if not version:
    raise RuntimeError('version is not defined')

readme = ''
with open(f'{path}/README.rst', encoding='UTF8') as f:
    readme = f.read()

setup(
    name='koreanbots',
    version=version,
    packages=['koreanbots'],
    license='MIT',
    description='A Simple Python API wrapper for KoreanBots.',
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
