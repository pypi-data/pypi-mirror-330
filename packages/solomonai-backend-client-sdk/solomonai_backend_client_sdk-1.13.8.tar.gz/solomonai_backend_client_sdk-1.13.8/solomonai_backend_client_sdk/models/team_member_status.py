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


class TeamMemberStatus(str, Enum):
    """
    Status of a team member within a team.   - TEAM_MEMBER_STATUS_UNSPECIFIED: Default unspecified status.  - TEAM_MEMBER_STATUS_ACTIVE: Member is active.  - TEAM_MEMBER_STATUS_INVITED: Member has been invited but not joined.  - TEAM_MEMBER_STATUS_PENDING: Member's request is pending approval.  - TEAM_MEMBER_STATUS_DECLINED: Member declined the invitation.  - TEAM_MEMBER_STATUS_REMOVED: Member was removed from the team.  - TEAM_MEMBER_STATUS_SUSPENDED: Member's account is suspended.
    """

    """
    allowed enum values
    """
    TEAM_MEMBER_STATUS_UNSPECIFIED = 'TEAM_MEMBER_STATUS_UNSPECIFIED'
    TEAM_MEMBER_STATUS_ACTIVE = 'TEAM_MEMBER_STATUS_ACTIVE'
    TEAM_MEMBER_STATUS_INVITED = 'TEAM_MEMBER_STATUS_INVITED'
    TEAM_MEMBER_STATUS_PENDING = 'TEAM_MEMBER_STATUS_PENDING'
    TEAM_MEMBER_STATUS_DECLINED = 'TEAM_MEMBER_STATUS_DECLINED'
    TEAM_MEMBER_STATUS_REMOVED = 'TEAM_MEMBER_STATUS_REMOVED'
    TEAM_MEMBER_STATUS_SUSPENDED = 'TEAM_MEMBER_STATUS_SUSPENDED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TeamMemberStatus from a JSON string"""
        return cls(json.loads(json_str))


