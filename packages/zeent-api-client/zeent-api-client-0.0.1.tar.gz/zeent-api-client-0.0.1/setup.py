# Packaging setup
from setuptools import setup, find_packages

setup(
    name="zeent-api-client",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "httpx"
    ],
    author="Joan Camps Morey",
    author_email="joan.camps@zeent.com",
    description="A reusable API client using httpx",
    url="https://github.com/zeent/zeent-api-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)