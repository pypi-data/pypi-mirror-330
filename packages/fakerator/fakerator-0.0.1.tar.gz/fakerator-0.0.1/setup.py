from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="fakerator",
    version="0.0.1",
    author="Evandro Systems",
    description="A simple faker library for python",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/evandrosystems/fakerpy",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)