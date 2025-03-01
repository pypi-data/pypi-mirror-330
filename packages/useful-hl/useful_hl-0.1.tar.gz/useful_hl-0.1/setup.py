from setuptools import setup, find_packages

setup(
    name="useful--hl",
    version="0.1",
    packages=find_packages(),
    install_requires=[
    "numpy==2.1.1","pylibCZIrw==4.1.3"],
    author="ktsolakidis",
    description="A simple package with random functions",
    python_requires=">=3.10,<3.11",  
)