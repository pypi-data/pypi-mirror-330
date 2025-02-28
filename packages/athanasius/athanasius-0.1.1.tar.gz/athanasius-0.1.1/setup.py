# setup.py
from setuptools import setup, find_packages

setup(
    name="athanasius",
    version="0.1.1",
    description="python CLI to archiving files",
    author="James",
    url="https://github.com/lim-james/athanasius",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ath=athanasius.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
