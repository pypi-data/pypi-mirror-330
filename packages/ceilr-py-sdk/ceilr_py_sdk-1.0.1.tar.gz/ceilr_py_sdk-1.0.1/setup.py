from setuptools import setup, find_packages

setup(
    name="ceilr-py-sdk",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["requests"],
    description="CeilR Python SDK for feature access, usage tracking, and entitlements",
    author="Mani Kumar Gouni",
    author_email="support@ceilr.com",
    license="MIT",
    url="https://github.com/GouniManikumar12/ceilr-py-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
