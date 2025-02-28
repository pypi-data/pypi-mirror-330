# Packaging setup
from setuptools import setup, find_packages

setup(
    name="apibench",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "httpx"
    ],
    author="Joan Camps Morey",
    author_email="joan.camps@zeent.com",
    description="A reusable API library using httpx",
    url="https://github.com/zeent/apibench",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)