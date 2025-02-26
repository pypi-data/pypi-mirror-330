from setuptools import setup, find_packages

setup(
    name="notunsplash",
    version="0.1.0",
    description="A Python SDK for the Unsplash API",
    author="Robert Jones",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
        "urllib3>=2.0.7",
    ],
    python_requires=">=3.7",
)
