from setuptools import setup, find_packages
from os import path
from datetime import datetime
now = datetime.now()
dt_string = now.strftime('%Y%m%d.%H%M')

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ed_design',
    version='1.1.0',
    author="Martin Vidkjaer",
    author_email="mav@envidan.dk",
    description="Python package developed by Envidan A/S scoping to follow the design of the company brand. This package is only for internal use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/EnviDan-AS/ed_design",
    packages=find_packages(),

    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'seaborn',
        'os',
        'platform',
    ],
    python_requires='>3.0.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Include package data specified in MANIFEST.in
    # package_data={'': ['ed_design/style']},
)
