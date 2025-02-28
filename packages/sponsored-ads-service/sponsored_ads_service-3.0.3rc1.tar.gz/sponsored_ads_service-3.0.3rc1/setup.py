import os

from setuptools import find_packages, setup

# with open("version") as fd:
#     version = fd.read().strip()

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()

setup(
    name="sponsored-ads-service",
    version="3.0.3rc1",
    description="S4F service responsible for sponsored ads",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],
    author="DSCBE",
    author_email="en-dsc-be@takealot.com",
    url="https://github.com/TAKEALOT/sponsored-ads-service",
    packages=find_packages(),
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "sponsored_ads_service=sponsored_ads_service.service:serve",
            "sponsored_ads_cli=sponsored_ads_service.cli:cli",
        ]
    },
)
