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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class WorkspaceservicehttpTusHeaders(BaseModel):
    """
    WorkspaceservicehttpTusHeaders
    """ # noqa: E501
    cache_control: Optional[StrictStr] = Field(default=None, description="Standard headers", alias="cacheControl")
    content_type: Optional[StrictStr] = Field(default=None, description="Must be application/offset+octet-stream for PATCH", alias="contentType")
    location: Optional[StrictStr] = Field(default=None, description="URL for the created resource")
    tus_checksum_algorithm: Optional[StrictStr] = Field(default=None, description="Comma-separated list of supported checksum algorithms", alias="tusChecksumAlgorithm")
    tus_extension: Optional[StrictStr] = Field(default=None, description="Extension headers", alias="tusExtension")
    tus_max_size: Optional[StrictInt] = Field(default=None, description="Maximum allowed upload size", alias="tusMaxSize")
    tus_resumable: StrictStr = Field(description="Core protocol headers", alias="tusResumable")
    tus_version: Optional[StrictStr] = Field(default=None, description="Comma-separated list of supported protocol versions", alias="tusVersion")
    upload_checksum: Optional[StrictStr] = Field(default=None, description="Algorithm and Base64 encoded checksum", alias="uploadChecksum")
    upload_concat: Optional[StrictStr] = Field(default=None, description="Concatenation information", alias="uploadConcat")
    upload_defer_length: Optional[StrictInt] = Field(default=None, description="Indicates deferred length (must be 1)", alias="uploadDeferLength")
    upload_expires: Optional[StrictStr] = Field(default=None, description="When the upload will expire", alias="uploadExpires")
    upload_length: Optional[StrictInt] = Field(default=None, description="Total size of the upload", alias="uploadLength")
    upload_metadata: Optional[StrictStr] = Field(default=None, description="Base64 encoded key-value pairs", alias="uploadMetadata")
    upload_offset: Optional[StrictInt] = Field(default=None, description="Current offset of the upload", alias="uploadOffset")
    __properties: ClassVar[List[str]] = ["cacheControl", "contentType", "location", "tusChecksumAlgorithm", "tusExtension", "tusMaxSize", "tusResumable", "tusVersion", "uploadChecksum", "uploadConcat", "uploadDeferLength", "uploadExpires", "uploadLength", "uploadMetadata", "uploadOffset"]

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
        """Create an instance of WorkspaceservicehttpTusHeaders from a JSON string"""
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
        """Create an instance of WorkspaceservicehttpTusHeaders from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "cacheControl": obj.get("cacheControl"),
            "contentType": obj.get("contentType"),
            "location": obj.get("location"),
            "tusChecksumAlgorithm": obj.get("tusChecksumAlgorithm"),
            "tusExtension": obj.get("tusExtension"),
            "tusMaxSize": obj.get("tusMaxSize"),
            "tusResumable": obj.get("tusResumable"),
            "tusVersion": obj.get("tusVersion"),
            "uploadChecksum": obj.get("uploadChecksum"),
            "uploadConcat": obj.get("uploadConcat"),
            "uploadDeferLength": obj.get("uploadDeferLength"),
            "uploadExpires": obj.get("uploadExpires"),
            "uploadLength": obj.get("uploadLength"),
            "uploadMetadata": obj.get("uploadMetadata"),
            "uploadOffset": obj.get("uploadOffset")
        })
        return _obj


