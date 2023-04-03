import sys
from setuptools import setup, find_packages

install_requires = [
    "azure-storage-blob==12.11.0",
    "boto3==1.22.8",
    "botocore==1.25.8",
    "frictionless==4.40.5",
    "psycopg2-binary==2.9.3",
    "pyarrow==7.0.0",
    "pydantic==1.9.1",
    "pyodbc==4.0.32",
    "requests==2.27.1",
    "SQLAlchemy==1.4.36",
]

if sys.version_info[1] == 7:
    install_requires.append("pandas==1.3.5")
else:
    install_requires.append("pandas==1.4.2")

setup(
    name="datajudge",
    version="",
    author="",
    author_email="",
    description="A framework to monitor data quality processes.",
    install_requires=install_requires,
    extras_require={
        "all": [
            "duckdb==0.4.0",
            "pandas-profiling==3.2.0",
            "great-expectations==0.15.14",
            ],
    },
    packages=find_packages()
)
