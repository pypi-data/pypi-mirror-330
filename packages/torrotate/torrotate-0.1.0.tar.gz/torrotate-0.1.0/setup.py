from setuptools import setup, find_packages

setup(
    name="torrotate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "stem>=1.8.0",
    ],
    python_requires=">=3.7",
)