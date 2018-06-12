from setuptools import setup, find_packages

PACKAGE_NAME = "vision"

setup(
    name=PACKAGE_NAME,
    version=open('vision/VERSION').readlines()[0].strip(),
    description='Simple receipt parser',
    author="Anandh Sridharan",
    author_email="anandhs@freshbooks.com",
    url="https://github.com/ajsridha/vision",
    packages=find_packages(exclude=['test', '*.test', '*.test.*']),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines()
)
