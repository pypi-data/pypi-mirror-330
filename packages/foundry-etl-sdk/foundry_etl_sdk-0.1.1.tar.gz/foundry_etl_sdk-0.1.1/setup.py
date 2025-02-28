from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="foundry_etl_sdk",
    version="0.1.1",
    packages=find_packages("src"),
    package_dir={'': 'src'},  
    install_requires=requirements,
)
