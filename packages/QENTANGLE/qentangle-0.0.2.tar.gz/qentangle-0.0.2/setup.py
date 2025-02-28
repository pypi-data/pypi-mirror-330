import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QENTANGLE",
    version="0.0.2",
    author="Center for Science Engagement,Barnas Monteith,Anna Du",
    author_email="barnas@engagescience.org",
    description="QENTANGLE Quantum education library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brn378/qentangle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
)
