from setuptools import setup, find_packages

setup(
    name="bns_geometry3d",
    version="0.1.0",
    author="Bholay Nath Singh",
    author_email="bholaynathsingh335619@gmail.com",
    description="A Python package for calculating surface areas of 3D shapes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
