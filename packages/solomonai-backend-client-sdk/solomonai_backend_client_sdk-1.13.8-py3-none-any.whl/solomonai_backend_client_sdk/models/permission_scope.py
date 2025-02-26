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


class PermissionScope(str, Enum):
    """
    - PERMISSION_SCOPE_UNSPECIFIED: Default value as required by proto3  - PERMISSION_SCOPE_TEAM: Permission applies to the team only  - PERMISSION_SCOPE_IMMEDIATE_HIERARCHY: Permission applies to the team and immediate sub-teams  - PERMISSION_SCOPE_FULL_HIERARCHY: Permission applies to the team and all sub-teams  - PERMISSION_SCOPE_RESOURCE_SPECIFIC: Permission applies to specific resources only
    """

    """
    allowed enum values
    """
    PERMISSION_SCOPE_UNSPECIFIED = 'PERMISSION_SCOPE_UNSPECIFIED'
    PERMISSION_SCOPE_TEAM = 'PERMISSION_SCOPE_TEAM'
    PERMISSION_SCOPE_IMMEDIATE_HIERARCHY = 'PERMISSION_SCOPE_IMMEDIATE_HIERARCHY'
    PERMISSION_SCOPE_FULL_HIERARCHY = 'PERMISSION_SCOPE_FULL_HIERARCHY'
    PERMISSION_SCOPE_RESOURCE_SPECIFIC = 'PERMISSION_SCOPE_RESOURCE_SPECIFIC'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PermissionScope from a JSON string"""
        return cls(json.loads(json_str))


