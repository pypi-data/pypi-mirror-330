# tenzro-trust/setup.py

from setuptools import setup, find_packages

setup(
    name="tenzro-trust",
    version="0.1.0",
    packages=find_packages(),
    description="Tenzro Trust: A modular, extensible hardware-rooted trust framework for distributed ledger systems, HSMs, TPMs, TEEs, Secure Enclaves, and more",
    author="Hilal Agil",
    author_email="hilal@tenzro.com",
    url="https://github.com/tenzro/tenzro-trust",
    license="MIT",
    install_requires=[
        "cryptography>=3.4.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)