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


class NotFoundErrorCode(str, Enum):
    """
    - NO_NOT_FOUND_ERROR: Default value as per proto3 convention  - UNDEFINED_ENDPOINT: Endpoint errors  Requested endpoint doesn't exist  - UNIMPLEMENTED: Endpoint not implemented  - STORE_ID_NOT_FOUND: Resource errors  Requested store ID doesn't exist  - USER_NOT_FOUND: Requested user doesn't exist  - RESOURCE_NOT_FOUND: Generic resource not found  - TENANT_NOT_FOUND: Requested tenant doesn't exist
    """

    """
    allowed enum values
    """
    NO_NOT_FOUND_ERROR = 'NO_NOT_FOUND_ERROR'
    UNDEFINED_ENDPOINT = 'UNDEFINED_ENDPOINT'
    UNIMPLEMENTED = 'UNIMPLEMENTED'
    STORE_ID_NOT_FOUND = 'STORE_ID_NOT_FOUND'
    USER_NOT_FOUND = 'USER_NOT_FOUND'
    RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
    TENANT_NOT_FOUND = 'TENANT_NOT_FOUND'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of NotFoundErrorCode from a JSON string"""
        return cls(json.loads(json_str))


