# -*- coding: utf-8 -*-

import os

from setuptools import setup

import koreanbots

version = koreanbots.__version__

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

requirements = []
with open(f"{path}/requirements.txt", encoding="UTF8") as f:
    requirements = f.read().splitlines()

if not version:
    raise RuntimeError("version is not defined")

readme = ""
with open(f"{path}/README.md", encoding="UTF8") as f:
    readme = f.read()

setup(
    name="koreanbots",
    author="Koreanbots",
    url="https://github.com/koreanbots/py-sdk",
    project_urls={
        "Homepage": "https://koreanbots.dev/",
        "Source": "https://github.com/koreanbots/py-sdk",
        "Tracker": "https://github.com/koreanbots/py-sdk/issues",
    },
    version=version,
    packages=["koreanbots"],
    license="MIT",
    description="Official SDK for Koreanbots.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    package_data={"koreanbots": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
