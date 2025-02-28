from setuptools import setup, find_packages

setup(
    name="hydra-search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "torch"
    ],
    author="Abhishek Pandey",
    author_email="abhshkpandey01@gmail.com",
    description="An advanced pathfinding algorithm inspired by the Hydra mechanism.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abhshkpandey/hydra-search",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
