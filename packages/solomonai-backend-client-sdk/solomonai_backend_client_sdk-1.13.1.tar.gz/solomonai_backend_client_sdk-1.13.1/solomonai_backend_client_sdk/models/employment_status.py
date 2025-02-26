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


class EmploymentStatus(str, Enum):
    """
    EmploymentStatus
    """

    """
    allowed enum values
    """
    EMPLOYMENT_STATUS_UNSPECIFIED = 'EMPLOYMENT_STATUS_UNSPECIFIED'
    EMPLOYMENT_STATUS_ACTIVE = 'EMPLOYMENT_STATUS_ACTIVE'
    EMPLOYMENT_STATUS_PENDING = 'EMPLOYMENT_STATUS_PENDING'
    EMPLOYMENT_STATUS_INACTIVE = 'EMPLOYMENT_STATUS_INACTIVE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of EmploymentStatus from a JSON string"""
        return cls(json.loads(json_str))


