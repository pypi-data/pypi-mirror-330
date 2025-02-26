# setup.py
from setuptools import setup, find_packages

setup(
    name="my_sample_package",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[ 
    ],
    description="A sample package to query tables in Azure Synapse using Spark SQL.",
    author="FlorianThoen",
    author_email="floiran.thoen@datarootsio.onmicrosoft.com",
    url="https://github.com/packageEVS"  # or any public/private repo
)
