# coding: utf-8

"""
    User Service API

    Solomon AI User Service API - Manages user profiles and authentication

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@solomon-ai.co
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class LocationType(str, Enum):
    """
    The location's type. Can be either WORK or HOME Possible values include: HOME, WORK. In cases where there is no clear mapping, the original value passed through will be returned.
    """

    """
    allowed enum values
    """
    LOCATION_TYPE_UNSPECIFIED = 'LOCATION_TYPE_UNSPECIFIED'
    LOCATION_TYPE_HOME = 'LOCATION_TYPE_HOME'
    LOCATION_TYPE_WORK = 'LOCATION_TYPE_WORK'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of LocationType from a JSON string"""
        return cls(json.loads(json_str))


