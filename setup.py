from setuptools import setup, find_packages

PACKAGE_NAME = "vision"

setup(
    name=PACKAGE_NAME,
    version=open('vision/VERSION').readlines()[0].strip(),
    description='Simple receipt parser',
    author="Anandh Sridharan",
    author_email="anandhs@freshbooks.com",
    packages=find_packages(exclude=['*.test', '*.test.*']),
    include_package_data=True
)
