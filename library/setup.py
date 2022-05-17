import sys
from setuptools import setup, find_packages

install_requires = [
    "azure-storage-blob==12.11.0",
    "boto3==1.22.8",
    "botocore==1.25.8",
    "psycopg2-binary==2.9.3",
    "pyarrow==7.0.0",
    "pydantic==1.9.0",
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
    version="1.0.0",
    author="",
    author_email="",
    description="A framework to monitor the data validation process.",
    install_requires=install_requires,
    extras_require={
        "all": [
            "duckdb==0.3.4",
            "frictionless==4.37.0",
            "pandas-profiling==3.2.0",
            ],
    },
    packages=find_packages()
)
