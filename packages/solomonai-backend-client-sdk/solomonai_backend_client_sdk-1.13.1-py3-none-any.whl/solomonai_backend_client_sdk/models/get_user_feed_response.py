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
from solomonai_backend_client_sdk.models.base_timeline import BaseTimeline
from solomonai_backend_client_sdk.models.notification_timeline import NotificationTimeline
from typing import Optional, Set
from typing_extensions import Self

class GetUserFeedResponse(BaseModel):
    """
    GetUserFeedResponse
    """ # noqa: E501
    base_timeline: Optional[BaseTimeline] = Field(default=None, alias="baseTimeline")
    notification_timeline: Optional[NotificationTimeline] = Field(default=None, alias="notificationTimeline")
    next_page_token: Optional[StrictStr] = Field(default=None, alias="nextPageToken")
    __properties: ClassVar[List[str]] = ["baseTimeline", "notificationTimeline", "nextPageToken"]

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
        """Create an instance of GetUserFeedResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of base_timeline
        if self.base_timeline:
            _dict['baseTimeline'] = self.base_timeline.to_dict()
        # override the default output from pydantic by calling `to_dict()` of notification_timeline
        if self.notification_timeline:
            _dict['notificationTimeline'] = self.notification_timeline.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetUserFeedResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "baseTimeline": BaseTimeline.from_dict(obj["baseTimeline"]) if obj.get("baseTimeline") is not None else None,
            "notificationTimeline": NotificationTimeline.from_dict(obj["notificationTimeline"]) if obj.get("notificationTimeline") is not None else None,
            "nextPageToken": obj.get("nextPageToken")
        })
        return _obj


