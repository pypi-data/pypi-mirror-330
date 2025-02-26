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
from solomonai_backend_client_sdk.models.user_tags import UserTags
from typing import Optional, Set
from typing_extensions import Self

class UserProfile(BaseModel):
    """
    UserProfile
    """ # noqa: E501
    id: Optional[StrictStr] = None
    tags: List[UserTags]
    name: StrictStr
    private: StrictBool
    followers: StrictStr
    following: StrictStr
    notification_feed_timeline_id: StrictStr = Field(alias="notificationFeedTimelineId")
    personal_feed_timeline_id: StrictStr = Field(alias="personalFeedTimelineId")
    news_feed_timeline_id: StrictStr = Field(alias="newsFeedTimelineId")
    profile_image_url: StrictStr = Field(alias="profileImageUrl")
    bookmarks: Bookmark
    algolia_id: StrictStr = Field(alias="algoliaId")
    __properties: ClassVar[List[str]] = ["id", "tags", "name", "private", "followers", "following", "notificationFeedTimelineId", "personalFeedTimelineId", "newsFeedTimelineId", "profileImageUrl", "bookmarks", "algoliaId"]

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
        """Create an instance of UserProfile from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        # override the default output from pydantic by calling `to_dict()` of bookmarks
        if self.bookmarks:
            _dict['bookmarks'] = self.bookmarks.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserProfile from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "tags": [UserTags.from_dict(_item) for _item in obj["tags"]] if obj.get("tags") is not None else None,
            "name": obj.get("name"),
            "private": obj.get("private"),
            "followers": obj.get("followers"),
            "following": obj.get("following"),
            "notificationFeedTimelineId": obj.get("notificationFeedTimelineId"),
            "personalFeedTimelineId": obj.get("personalFeedTimelineId"),
            "newsFeedTimelineId": obj.get("newsFeedTimelineId"),
            "profileImageUrl": obj.get("profileImageUrl"),
            "bookmarks": Bookmark.from_dict(obj["bookmarks"]) if obj.get("bookmarks") is not None else None,
            "algoliaId": obj.get("algoliaId")
        })
        return _obj

from solomonai_backend_client_sdk.models.bookmark import Bookmark
# TODO: Rewrite to not use raise_errors
UserProfile.model_rebuild(raise_errors=False)

