from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('discord/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not defined')

setup(
    name='koreanbots',
    author='kijk2869',
    url='https://github.com/Rapptz/discord.py',
    project_urls={
        "Documentation": "https://discordpy.readthedocs.io/en/latest/"
    },
    version=version,
    packages=['koreanbots'],
    license='MIT',
    description='A Python wrapper for the KoreanBots API',
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