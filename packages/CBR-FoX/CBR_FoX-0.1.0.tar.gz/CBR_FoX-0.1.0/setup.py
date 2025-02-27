from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="CBR_FoX",
    version="0.1.0",
    description = "A case-based reasoning python library that aims to help researchers find similar cases according to an input case with a wide range of methods that can detect similarity based on the features of each time series",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.7",
)

