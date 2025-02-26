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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class Contacts(BaseModel):
    """
    The Contact object refers to either a supplier or a customer.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    remote_id: Optional[StrictStr] = Field(default=None, description="The third-party API ID of the matching object.", alias="remoteId")
    name: Optional[StrictStr] = Field(default=None, description="The contact's name.")
    is_supplier: Optional[StrictBool] = Field(default=None, description="Whether the contact is a supplier.", alias="isSupplier")
    is_customer: Optional[StrictBool] = Field(default=None, description="Whether the contact is a customer.", alias="isCustomer")
    email_address: Optional[StrictStr] = Field(default=None, description="The contact's email address.", alias="emailAddress")
    tax_number: Optional[StrictStr] = Field(default=None, description="The contact's tax number.", alias="taxNumber")
    status: Optional[StrictStr] = None
    currency: Optional[StrictStr] = Field(default=None, description="The currency the contact's transactions are in.")
    remote_updated_at: Optional[datetime] = Field(default=None, description="When the third party's contact was updated.  Consider using google.protobuf.Timestamp", alias="remoteUpdatedAt")
    company: Optional[StrictStr] = Field(default=None, description="The company the contact belongs to.")
    addresses_ids: Optional[List[StrictStr]] = Field(default=None, description="Address object IDs for the given Contacts object.  These are IDs, not the Address structure itself", alias="addressesIds")
    phone_numbers: Optional[List[StrictStr]] = Field(default=None, alias="phoneNumbers")
    remote_was_deleted: Optional[StrictBool] = Field(default=None, description="Indicates whether or not this object has been deleted by third party webhooks.", alias="remoteWasDeleted")
    modified_at: Optional[datetime] = Field(default=None, description="Consider using google.protobuf.Timestamp", alias="modifiedAt")
    merge_record_id: Optional[StrictStr] = Field(default=None, alias="mergeRecordId")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    __properties: ClassVar[List[str]] = ["id", "remoteId", "name", "isSupplier", "isCustomer", "emailAddress", "taxNumber", "status", "currency", "remoteUpdatedAt", "company", "addressesIds", "phoneNumbers", "remoteWasDeleted", "modifiedAt", "mergeRecordId", "createdAt", "deletedAt"]

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
        """Create an instance of Contacts from a JSON string"""
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
        """Create an instance of Contacts from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "remoteId": obj.get("remoteId"),
            "name": obj.get("name"),
            "isSupplier": obj.get("isSupplier"),
            "isCustomer": obj.get("isCustomer"),
            "emailAddress": obj.get("emailAddress"),
            "taxNumber": obj.get("taxNumber"),
            "status": obj.get("status"),
            "currency": obj.get("currency"),
            "remoteUpdatedAt": obj.get("remoteUpdatedAt"),
            "company": obj.get("company"),
            "addressesIds": obj.get("addressesIds"),
            "phoneNumbers": obj.get("phoneNumbers"),
            "remoteWasDeleted": obj.get("remoteWasDeleted"),
            "modifiedAt": obj.get("modifiedAt"),
            "mergeRecordId": obj.get("mergeRecordId"),
            "createdAt": obj.get("createdAt"),
            "deletedAt": obj.get("deletedAt")
        })
        return _obj


