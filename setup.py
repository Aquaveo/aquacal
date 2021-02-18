from setuptools import setup, find_packages

requirements = [
    'requests'
]

setup(
    name='aquacal',
    version='1.0.0',
    description='Calendar utilities for Aquaveo',
    author='Nathan Swain',
    author_email='nswain@aquaveo.com',
    url='https://www.aquaveo.com',
    packages=find_packages(exclude='tests'),
    requires=requirements
)
