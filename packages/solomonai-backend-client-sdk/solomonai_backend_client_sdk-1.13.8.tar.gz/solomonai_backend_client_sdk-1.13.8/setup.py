# coding: utf-8

"""
    Lead Scraping Service API

    Vector Lead Scraping Service API - Manages Lead Scraping Jobs

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@vector.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "solomonai-backend-client-sdk"
VERSION = "1.13.8"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Solomonai Backend Client SDK",
    author="Solomonai Engineering",
    author_email="yoanyomba@solomonai.co",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Solomonai Backend Client SDK"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache 2.0 License",
    long_description_content_type='text/markdown',
    long_description="""\
    Solomonai Backend Client SDK
    """,  # noqa: E501
    package_data={"solomonai-backend-client-sdk": ["py.typed"]},
)
