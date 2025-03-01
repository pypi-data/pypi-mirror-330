# tenzro-store/setup.py

from setuptools import setup, find_packages

setup(
    name="tenzro-store",
    version="0.1.1",
    packages=find_packages(),
    description="Tenzro Store: A modular, extensible storage system for distributed ledger systems, storing data in .tzds files",
    author="Hilal Agil",
    author_email="hilaal@gmail.com",
    url="https://github.com/tenzro/tenzro-store",
    license="MIT",
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)