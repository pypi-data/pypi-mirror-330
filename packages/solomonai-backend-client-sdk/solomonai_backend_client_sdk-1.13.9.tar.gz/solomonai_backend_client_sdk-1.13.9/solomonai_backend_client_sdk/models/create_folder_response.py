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

class CreateFolderResponse(BaseModel):
    """
    CreateFolderResponse represents the response returned after successfully creating a new folder. This message provides comprehensive details about the newly created folder structure, including its metadata and organizational context.  Key features: - Complete folder metadata - Hierarchical information - Access control details - Creation timestamps - Storage location details  Usage example: The response includes a FolderMetadata object containing all necessary information about the created folder, such as: - Unique folder identifier - Parent folder relationship - Creation and modification timestamps - Access permissions - Storage path information
    """ # noqa: E501
    folder: Optional[FolderMetadata] = None
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
        """Create an instance of CreateFolderResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of folder
        if self.folder:
            _dict['folder'] = self.folder.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateFolderResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "folder": FolderMetadata.from_dict(obj["folder"]) if obj.get("folder") is not None else None
        })
        return _obj


