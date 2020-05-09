from setuptools import setup
import re

version = ''
with open('koreanbots/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

if not version:
    raise RuntimeError('version is not defined')

readme = ''
with open('README.rst') as f:
    readme = f.read()

setup(
    name='koreanbots',
    author='kijk2869',
    url='https://github.com/kijk2869/koreanbots',
    project_urls={
        "Homepage": "https://koreanbots.cf/",
        "Source":"https://github.com/koreanbots/py-sdk",
        "Tracker":"https://github.com/koreanbots/py-sdk/issues"
    },
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
