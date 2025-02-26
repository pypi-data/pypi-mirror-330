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

from pydantic import BaseModel, ConfigDict
from typing import Any, ClassVar, Dict, List, Optional
from solomonai_backend_client_sdk.models.folder_metadata import FolderMetadata
from typing import Optional, Set
from typing_extensions import Self

class ListFolderResponse(BaseModel):
    """
    ListFolderResponse represents the response to a folder listing request. This message contains a list of folder metadata objects representing the folders found within the requested scope (workspace and parent folder context).  Key features: - Complete folder metadata for each folder - Hierarchical folder structure representation - Permission and access information included - Support for pagination results  Usage example: Used to display folder listings in a file explorer interface, showing folder hierarchies and metadata within a workspace.
    """ # noqa: E501
    folder: Optional[List[FolderMetadata]] = None
    __properties: ClassVar[List[str]] = ["folder"]

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
        """Create an instance of ListFolderResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in folder (list)
        _items = []
        if self.folder:
            for _item in self.folder:
                if _item:
                    _items.append(_item.to_dict())
            _dict['folder'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ListFolderResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "folder": [FolderMetadata.from_dict(_item) for _item in obj["folder"]] if obj.get("folder") is not None else None
        })
        return _obj


