from setuptools import find_packages, setup

with open("version") as fd:
    version = fd.read().strip()

setup(
    name="sponsored-ads-client",
    version=version,
    python_requires=">=3.9",
    description="S4F client responsible for the sponsored ads service",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
        "Intended Audience :: Takealot Developers",
    ],
    author="DSCBE",
    author_email="en-dsc-be@takealot.com",
    url="https://github.com/TAKEALOT/sponsored-ads-service",
    packages=find_packages(include=["sponsored_ads_client*"]),
    package_dir={"sponsored_ads_client": "sponsored_ads_client"},
    test_suite="tests",
    install_requires=["s4f", "protobuf"],
)
