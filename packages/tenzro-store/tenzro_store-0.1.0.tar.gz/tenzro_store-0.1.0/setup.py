# tenzro-store/setup.py

from setuptools import setup, find_packages

setup(
    name="tenzro-store",
    version="0.1.0",
    packages=find_packages(),
    description="Tenzro Store: A modular, extensible storage framework for distributed ledger systems, storing data in .tzds files",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/your-org/tenzro-store",
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