from setuptools import setup, find_packages

setup(
    name="solnir",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "pika",
    ],
)
