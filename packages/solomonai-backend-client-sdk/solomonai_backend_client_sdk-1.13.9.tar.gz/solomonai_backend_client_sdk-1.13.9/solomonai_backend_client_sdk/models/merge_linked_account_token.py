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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class MergeLinkedAccountToken(BaseModel):
    """
    MergeLinkedAccountToken
    """ # noqa: E501
    id: Optional[StrictStr] = None
    item_id: Optional[StrictStr] = Field(default=None, alias="itemId")
    key_id: Optional[StrictStr] = Field(default=None, alias="keyId")
    access_token: Optional[StrictStr] = Field(default=None, alias="accessToken")
    version: Optional[StrictStr] = None
    merge_end_user_origin_id: Optional[StrictStr] = Field(default=None, description="This is what you'll pass to Merge as the end_user_origin_id.", alias="mergeEndUserOriginId")
    merge_integration_slug: Optional[StrictStr] = Field(default=None, description="The integration slug/identifier. This is returned at the end of the linking flow.", alias="mergeIntegrationSlug")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    __properties: ClassVar[List[str]] = ["id", "itemId", "keyId", "accessToken", "version", "mergeEndUserOriginId", "mergeIntegrationSlug", "createdAt", "deletedAt"]

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
        """Create an instance of MergeLinkedAccountToken from a JSON string"""
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
        """Create an instance of MergeLinkedAccountToken from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "itemId": obj.get("itemId"),
            "keyId": obj.get("keyId"),
            "accessToken": obj.get("accessToken"),
            "version": obj.get("version"),
            "mergeEndUserOriginId": obj.get("mergeEndUserOriginId"),
            "mergeIntegrationSlug": obj.get("mergeIntegrationSlug"),
            "createdAt": obj.get("createdAt"),
            "deletedAt": obj.get("deletedAt")
        })
        return _obj


