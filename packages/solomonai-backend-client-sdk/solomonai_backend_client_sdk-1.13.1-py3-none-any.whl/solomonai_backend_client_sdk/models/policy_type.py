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


class PolicyType(str, Enum):
    """
    PolicyType
    """

    """
    allowed enum values
    """
    POLICY_TYPE_UNSPECIFIED = 'POLICY_TYPE_UNSPECIFIED'
    POLICY_TYPE_VACATION = 'POLICY_TYPE_VACATION'
    POLICY_TYPE_SICK = 'POLICY_TYPE_SICK'
    POLICY_TYPE_PERSONAL = 'POLICY_TYPE_PERSONAL'
    POLICY_TYPE_JURY_DUTY = 'POLICY_TYPE_JURY_DUTY'
    POLICY_TYPE_VOLUNTEER = 'POLICY_TYPE_VOLUNTEER'
    POLICY_TYPE_BEREAVEMENT = 'POLICY_TYPE_BEREAVEMENT'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PolicyType from a JSON string"""
        return cls(json.loads(json_str))


