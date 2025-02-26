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


class ProfileType(str, Enum):
    """
    Represents types of accounts linked to a profile.   - PROFILE_TYPE_UNSPECIFIED: Default unspecified profile type.  - PROFILE_TYPE_USER: Individual user profile.  - PROFILE_TYPE_BUSINESS: Business profile.
    """

    """
    allowed enum values
    """
    PROFILE_TYPE_UNSPECIFIED = 'PROFILE_TYPE_UNSPECIFIED'
    PROFILE_TYPE_USER = 'PROFILE_TYPE_USER'
    PROFILE_TYPE_BUSINESS = 'PROFILE_TYPE_BUSINESS'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ProfileType from a JSON string"""
        return cls(json.loads(json_str))


