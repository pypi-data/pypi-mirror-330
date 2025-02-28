#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

VERSION = '0.0.1'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements =[
    "click",
    "loguru",
    "pygithub",
    "gitpython",
    "pexpect",
    "toml"
]

test_requirements = ['pytest>=3']

setup(
    author="Rex Wang",
    author_email='1073853456@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="Interact with ChatGPT in terminal via chattool",
    install_requires=requirements,
    license="MIT license",
    # long_description=readme + '\n\n' + history ,
    include_package_data=True,
    keywords='filelean',
    name='filelean',
    entry_points="""
    [console_scripts]
    filelean=filelean.cli.main:cli
    """,
    packages=find_packages(include=['filelean', 'filelean.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Lean-zh/FileLean',
    version=VERSION,
    zip_safe=False,
)
