# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readmeContent = f.read()

with open('LICENSE') as f:
    licenseContent = f.read()

setup(
    name='alfred',
    version='0.0.1',
    description='Home automation robot',
    long_description=readmeContent,
    author='Mattias Jakobsson',
    author_email='mattias@jajoit.se',
    url='',
    license=licenseContent,
    packages=find_packages(exclude=('tests', 'docs'))
)
