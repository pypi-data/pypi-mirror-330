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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from solomonai_backend_client_sdk.models.workspaceservicehttp_checksum_info import WorkspaceservicehttpChecksumInfo
from solomonai_backend_client_sdk.models.workspaceservicehttp_storage_info import WorkspaceservicehttpStorageInfo
from typing import Optional, Set
from typing_extensions import Self

class WorkspaceservicehttpResourceInfo(BaseModel):
    """
    WorkspaceservicehttpResourceInfo
    """ # noqa: E501
    checksum: Optional[WorkspaceservicehttpChecksumInfo] = Field(default=None, description="Checksum information (if available)")
    created_at: Optional[StrictStr] = Field(default=None, description="Creation information", alias="createdAt")
    expires_at: Optional[StrictStr] = Field(default=None, alias="expiresAt")
    id: Optional[StrictStr] = Field(default=None, description="Resource identifier")
    is_final: Optional[StrictBool] = Field(default=None, description="Whether this is a final upload", alias="isFinal")
    is_partial: Optional[StrictBool] = Field(default=None, description="Whether this is a partial upload", alias="isPartial")
    length: Optional[StrictInt] = Field(default=None, description="Total size in bytes")
    metadata: Optional[Dict[str, StrictStr]] = Field(default=None, description="Upload metadata")
    offset: Optional[StrictInt] = Field(default=None, description="Current offset")
    parts: Optional[List[StrictStr]] = Field(default=None, description="URLs of partial uploads for final upload")
    storage: Optional[WorkspaceservicehttpStorageInfo] = Field(default=None, description="Storage information")
    __properties: ClassVar[List[str]] = ["checksum", "createdAt", "expiresAt", "id", "isFinal", "isPartial", "length", "metadata", "offset", "parts", "storage"]

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
        """Create an instance of WorkspaceservicehttpResourceInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of checksum
        if self.checksum:
            _dict['checksum'] = self.checksum.to_dict()
        # override the default output from pydantic by calling `to_dict()` of storage
        if self.storage:
            _dict['storage'] = self.storage.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorkspaceservicehttpResourceInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "checksum": WorkspaceservicehttpChecksumInfo.from_dict(obj["checksum"]) if obj.get("checksum") is not None else None,
            "createdAt": obj.get("createdAt"),
            "expiresAt": obj.get("expiresAt"),
            "id": obj.get("id"),
            "isFinal": obj.get("isFinal"),
            "isPartial": obj.get("isPartial"),
            "length": obj.get("length"),
            "metadata": obj.get("metadata"),
            "offset": obj.get("offset"),
            "parts": obj.get("parts"),
            "storage": WorkspaceservicehttpStorageInfo.from_dict(obj["storage"]) if obj.get("storage") is not None else None
        })
        return _obj


