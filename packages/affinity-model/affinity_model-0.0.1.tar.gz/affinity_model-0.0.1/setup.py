from setuptools import setup, find_packages

setup(
    name="affinity-model",
    version="0.0.1",
    author="Planet A GmbH",
    author_email="dev@planet-a.com",
    packages=find_packages(exclude=["tests"]),
    description="A data model for the Affinity CRM API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
