from setuptools import setup, find_packages

setup(
    name="datajudge",
    version="0.0.1",
    author="",
    author_email="",
    description="To write",
    install_requires=[
            "python-slugify>=4.0.1",
            "requests>=2.25.1",
            "boto3>=1.17.5",
            "botocore>=1.20.5",
            "frictionless>=4.9.0",
            "pandas>=1.2.4",
            "pandas-profiling>=2.11.0"],
    packages=find_packages()
)
