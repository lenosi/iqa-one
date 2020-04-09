# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup, find_packages

files = ["*"]

setup(
    name='iqa-one',
    version='0.1.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='Apache 2.0',
    description='Messaging testing project',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock', 'pytest-mock'],
    install_requires=[
        'ansible',
        'python-qpid-proton',
        'amqcfg',
        'dpath',
        'optconstruct',
        'docker',
        'urllib3',
        'kubernetes'
    ],
    url='https://github.com/enkeys/iqa-one',
    author='Dominik Lenoch',
    author_email='dlenoch@redhat.com'
)
