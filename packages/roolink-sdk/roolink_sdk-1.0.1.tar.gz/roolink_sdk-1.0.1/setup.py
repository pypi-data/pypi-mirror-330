from setuptools import setup, find_packages

setup(
    name="roolink-sdk",
    version="1.0.1",
    description="A Python SDK for interacting with the RooLink API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RooLinkIO/roolink-sdk-py",
    license="MIT",
    packages=find_packages(),
    install_requires=[
      "requests>=2.20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
