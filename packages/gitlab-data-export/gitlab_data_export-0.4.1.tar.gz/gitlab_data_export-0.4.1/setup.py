from setuptools import setup, find_packages
from typing import List
import os
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

requirements: List[str] = [
    'google-cloud-bigquery>=3.0.0,<3.20.0',
    'python-gitlab>=3.0.0,<4'
]

version = os.getenv('CI_COMMIT_TAG', 'v0.0.1').strip('v')

setup(
    name='gitlab_data_export',
    version=version,
    description='Export GitLab data to external data stores',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/belvederetrading/public/gitlab-data-export',
    author='Belvedere Trading',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=requirements,
    extras_require={
        'dev': ['autopep8', 'build', 'coverage', 'google-auth-stubs', 'mypy', 'python-dotenv', 'twine'],
    },
    entry_points={
        'console_scripts': [
            'gitlab-data-export=gitlab_data_export.driver:main'
        ],
    },
    project_urls={
        'Bug Reports': 'https://gitlab.com/belvederetrading/public/gitlab-data-export/-/issues',
        'Source': 'https://gitlab.com/belvederetrading/public/gitlab-data-export',
    },
)
