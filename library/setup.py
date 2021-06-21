from setuptools import setup, find_packages

setup(
    name="datajudge",
    version="1.0.0",
    author="",
    author_email="",
    description="A framework to monitor the data validation process.",
    install_requires=[
            "python-slugify>=4.0.1",
            "requests>=2.25.1",
            "boto3>=1.17.5",
            "botocore>=1.20.5",
            "pandas>=1.2.4",
            "pandas-profiling>=2.11.0",
            "azure-storage-blob>=12.8.1"],
    extras_require = {
        "all": ["frictionless>=4.9.0",],
        "frictionless": ["frictionless>=4.9.0",],
    },
    packages=find_packages()
)
