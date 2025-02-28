from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="foundry_db",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,  # Loads dependencies from requirements.txt
)
