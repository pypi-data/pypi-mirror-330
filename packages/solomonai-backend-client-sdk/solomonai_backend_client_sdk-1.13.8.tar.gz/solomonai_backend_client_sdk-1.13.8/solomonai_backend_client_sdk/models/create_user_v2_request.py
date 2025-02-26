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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from solomonai_backend_client_sdk.models.profile_type import ProfileType
from typing import Optional, Set
from typing_extensions import Self

class CreateUserV2Request(BaseModel):
    """
    CreateUserV2Request represents the request object for creating a user account in the user service (version 2). This message encapsulates all necessary information to create a user account, including authentication details, contact information, and profile preferences.
    """ # noqa: E501
    supabase_auth_user_id: StrictStr = Field(description="The Supabase authentication user ID associated with this account. This field is required and must not be empty.  @required This field must be provided when creating a user account. @validate Ensures that the Supabase auth user ID is not empty. @example \"auth0|5f7d8ff9d8f1f0006f3e9f1e\"", alias="supabaseAuthUserId")
    email: Optional[StrictStr] = Field(default=None, description="Email address associated with the user account. This field must contain a valid email address.  @validate Ensures that the provided string is a valid email address. @example \"john.doe@example.com\"")
    username: StrictStr = Field(description="Username associated with the account. This field is required and must not be empty.  @required This field must be provided when creating a user account. @validate Ensures that the username is not empty. @example \"johndoe2023\"")
    profile_type: ProfileType = Field(alias="profileType")
    profile_image_url: StrictStr = Field(description="URL of the user's profile image. This field is required and must be a valid URI.  @required This field must be provided when creating a user account. @validate Ensures that the provided URL is a valid URI. @example \"https://example.com/profile_images/johndoe.jpg\"", alias="profileImageUrl")
    organization_id: StrictStr = Field(alias="organizationId")
    tenant_id: StrictStr = Field(alias="tenantId")
    company_name: StrictStr = Field(alias="companyName")
    is_private: StrictBool = Field(alias="isPrivate")
    __properties: ClassVar[List[str]] = ["supabaseAuthUserId", "email", "username", "profileType", "profileImageUrl", "organizationId", "tenantId", "companyName", "isPrivate"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of CreateUserV2Request from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateUserV2Request from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "supabaseAuthUserId": obj.get("supabaseAuthUserId"),
            "email": obj.get("email"),
            "username": obj.get("username"),
            "profileType": obj.get("profileType") if obj.get("profileType") is not None else ProfileType.UNSPECIFIED,
            "profileImageUrl": obj.get("profileImageUrl"),
            "organizationId": obj.get("organizationId"),
            "tenantId": obj.get("tenantId"),
            "companyName": obj.get("companyName"),
            "isPrivate": obj.get("isPrivate")
        })
        return _obj


