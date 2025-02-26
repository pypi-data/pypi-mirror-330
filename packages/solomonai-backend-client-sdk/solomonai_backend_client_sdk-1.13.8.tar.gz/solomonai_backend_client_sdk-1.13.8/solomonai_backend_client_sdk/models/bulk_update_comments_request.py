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
from typing import Optional, Set
from typing_extensions import Self

class BulkUpdateCommentsRequest(BaseModel):
    """
    BulkUpdateCommentsRequest represents a request to update multiple comments.
    """ # noqa: E501
    user_id: StrictStr = Field(alias="userId")
    comment_ids: Optional[List[StrictStr]] = Field(default=None, alias="commentIds")
    workspace_id: StrictStr = Field(alias="workspaceId")
    folder_id: StrictStr = Field(alias="folderId")
    file_id: StrictStr = Field(alias="fileId")
    thread_id: StrictStr = Field(alias="threadId")
    status: Optional[StrictStr] = None
    add_tags: Optional[List[StrictStr]] = Field(default=None, alias="addTags")
    remove_tags: Optional[List[StrictStr]] = Field(default=None, alias="removeTags")
    org_id: StrictStr = Field(alias="orgId")
    tenant_id: StrictStr = Field(alias="tenantId")
    __properties: ClassVar[List[str]] = ["userId", "commentIds", "workspaceId", "folderId", "fileId", "threadId", "status", "addTags", "removeTags", "orgId", "tenantId"]

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
        """Create an instance of BulkUpdateCommentsRequest from a JSON string"""
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
        """Create an instance of BulkUpdateCommentsRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "userId": obj.get("userId"),
            "commentIds": obj.get("commentIds"),
            "workspaceId": obj.get("workspaceId"),
            "folderId": obj.get("folderId"),
            "fileId": obj.get("fileId"),
            "threadId": obj.get("threadId"),
            "status": obj.get("status"),
            "addTags": obj.get("addTags"),
            "removeTags": obj.get("removeTags"),
            "orgId": obj.get("orgId"),
            "tenantId": obj.get("tenantId")
        })
        return _obj


