from setuptools import setup, find_packages

setup(
    name="advdask",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="your-email@example.com",
    description="An advanced extension of the Dask library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/advdask",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "dask>=2023.0.0",
        "numpy>=1.15.0",
    ],
)