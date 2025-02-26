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


class IndustryType(str, Enum):
    """
    Represents various industries a business can belong to.   - INDUSTRY_TYPE_UNSPECIFIED: Default unspecified industry.  - INDUSTRY_TYPE_TECHNOLOGY: Technology sector.  - INDUSTRY_TYPE_FINANCE: Finance sector.  - INDUSTRY_TYPE_HEALTHCARE: Healthcare sector.  - INDUSTRY_TYPE_EDUCATION: Education sector.  - INDUSTRY_TYPE_RETAIL: Retail sector.  - INDUSTRY_TYPE_MANUFACTURING: Manufacturing sector.  - INDUSTRY_TYPE_OTHER: Other or unlisted industry.
    """

    """
    allowed enum values
    """
    INDUSTRY_TYPE_UNSPECIFIED = 'INDUSTRY_TYPE_UNSPECIFIED'
    INDUSTRY_TYPE_TECHNOLOGY = 'INDUSTRY_TYPE_TECHNOLOGY'
    INDUSTRY_TYPE_FINANCE = 'INDUSTRY_TYPE_FINANCE'
    INDUSTRY_TYPE_HEALTHCARE = 'INDUSTRY_TYPE_HEALTHCARE'
    INDUSTRY_TYPE_EDUCATION = 'INDUSTRY_TYPE_EDUCATION'
    INDUSTRY_TYPE_RETAIL = 'INDUSTRY_TYPE_RETAIL'
    INDUSTRY_TYPE_MANUFACTURING = 'INDUSTRY_TYPE_MANUFACTURING'
    INDUSTRY_TYPE_OTHER = 'INDUSTRY_TYPE_OTHER'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of IndustryType from a JSON string"""
        return cls(json.loads(json_str))


