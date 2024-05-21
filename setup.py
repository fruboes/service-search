#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["pandas", "openpyxl", "opensearch-py<3", "flask", "python-dotenv" ]

test_requirements = ['pytest>=3', ]

setup(
    author="Tomasz Fruboes",
    author_email='Tomasz.Fruboes@ncbj.gov.pl',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Simple service search for NCC Poland",
    entry_points={
        'console_scripts': [
            'cc_service_search=cc_service_search.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cc_service_search',
    name='cc_service_search',
    packages=find_packages(include=['cc_service_search', 'cc_service_search.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tfruboes/cc_service_search',
    version='1.0.0',
    zip_safe=False,
)
