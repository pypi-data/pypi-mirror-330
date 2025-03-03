from setuptools import setup, find_packages

setup(
    name="moalpy",
    author="LDATuan",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["numpy>=1.26.4", "scipy>=1.15.2", "matplotlib>=3.8.4", "pandas>=2.2.2"],
)