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


class SeverityLevel(str, Enum):
    """
    Levels of severity for logging or alerting.   - SEVERITY_LEVEL_UNSPECIFIED: Default unspecified level.  - SEVERITY_LEVEL_INFO: Informational message.  - SEVERITY_LEVEL_WARNING: Warning message.  - SEVERITY_LEVEL_ERROR: Error message.  - SEVERITY_LEVEL_CRITICAL: Critical failure message.
    """

    """
    allowed enum values
    """
    SEVERITY_LEVEL_UNSPECIFIED = 'SEVERITY_LEVEL_UNSPECIFIED'
    SEVERITY_LEVEL_INFO = 'SEVERITY_LEVEL_INFO'
    SEVERITY_LEVEL_WARNING = 'SEVERITY_LEVEL_WARNING'
    SEVERITY_LEVEL_ERROR = 'SEVERITY_LEVEL_ERROR'
    SEVERITY_LEVEL_CRITICAL = 'SEVERITY_LEVEL_CRITICAL'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of SeverityLevel from a JSON string"""
        return cls(json.loads(json_str))


