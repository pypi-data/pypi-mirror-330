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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from solomonai_backend_client_sdk.models.account_type import AccountType
from solomonai_backend_client_sdk.models.media import Media
from typing import Optional, Set
from typing_extensions import Self

class Note(BaseModel):
    """
    Note
    """ # noqa: E501
    id: Optional[StrictStr] = None
    backend_platform_user_id: Optional[StrictStr] = Field(default=None, alias="backendPlatformUserId")
    profile_id: Optional[StrictStr] = Field(default=None, alias="profileId")
    media: Optional[Media] = None
    mentions: Optional[List[StrictStr]] = None
    hashtags: Optional[List[StrictStr]] = None
    created_at: Optional[StrictStr] = Field(default=None, alias="createdAt")
    content: StrictStr
    author_account_type: Optional[AccountType] = Field(default=AccountType.UNSPECIFIED, alias="authorAccountType")
    author_user_name: StrictStr = Field(alias="authorUserName")
    author_profile_image: StrictStr = Field(alias="authorProfileImage")
    __properties: ClassVar[List[str]] = ["id", "backendPlatformUserId", "profileId", "media", "mentions", "hashtags", "createdAt", "content", "authorAccountType", "authorUserName", "authorProfileImage"]

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
        """Create an instance of Note from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of media
        if self.media:
            _dict['media'] = self.media.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Note from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "backendPlatformUserId": obj.get("backendPlatformUserId"),
            "profileId": obj.get("profileId"),
            "media": Media.from_dict(obj["media"]) if obj.get("media") is not None else None,
            "mentions": obj.get("mentions"),
            "hashtags": obj.get("hashtags"),
            "createdAt": obj.get("createdAt"),
            "content": obj.get("content"),
            "authorAccountType": obj.get("authorAccountType") if obj.get("authorAccountType") is not None else AccountType.UNSPECIFIED,
            "authorUserName": obj.get("authorUserName"),
            "authorProfileImage": obj.get("authorProfileImage")
        })
        return _obj


