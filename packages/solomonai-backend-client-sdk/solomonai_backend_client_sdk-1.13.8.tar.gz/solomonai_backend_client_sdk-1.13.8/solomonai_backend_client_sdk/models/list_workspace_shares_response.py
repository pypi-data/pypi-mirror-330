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
from solomonai_backend_client_sdk.models.workspace_sharing import WorkspaceSharing
from typing import Optional, Set
from typing_extensions import Self

class ListWorkspaceSharesResponse(BaseModel):
    """
    ListWorkspaceSharesResponse represents the response containing a list of workspace shares. Includes pagination information for handling large result sets.  Fields: - shares: List of WorkspaceSharing objects containing share details - next_page_number: Page number for retrieving the next set of results
    """ # noqa: E501
    shares: Optional[List[WorkspaceSharing]] = None
    next_page_number: Optional[StrictStr] = Field(default=None, alias="nextPageNumber")
    __properties: ClassVar[List[str]] = ["shares", "nextPageNumber"]

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
        """Create an instance of ListWorkspaceSharesResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in shares (list)
        _items = []
        if self.shares:
            for _item in self.shares:
                if _item:
                    _items.append(_item.to_dict())
            _dict['shares'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ListWorkspaceSharesResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "shares": [WorkspaceSharing.from_dict(_item) for _item in obj["shares"]] if obj.get("shares") is not None else None,
            "nextPageNumber": obj.get("nextPageNumber")
        })
        return _obj


