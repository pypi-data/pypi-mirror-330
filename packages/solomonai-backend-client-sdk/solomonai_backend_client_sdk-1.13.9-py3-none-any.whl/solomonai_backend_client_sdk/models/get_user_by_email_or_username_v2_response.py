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
from solomonai_backend_client_sdk.models.business_account import BusinessAccount
from solomonai_backend_client_sdk.models.user_account import UserAccount
from typing import Optional, Set
from typing_extensions import Self

class GetUserByEmailOrUsernameV2Response(BaseModel):
    """
    GetUserByEmailOrUsernameV2Response
    """ # noqa: E501
    user_account: Optional[UserAccount] = Field(default=None, alias="userAccount")
    business_account: Optional[BusinessAccount] = Field(default=None, alias="businessAccount")
    sso_token: Optional[StrictStr] = Field(default=None, alias="ssoToken")
    __properties: ClassVar[List[str]] = ["userAccount", "businessAccount", "ssoToken"]

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
        """Create an instance of GetUserByEmailOrUsernameV2Response from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of user_account
        if self.user_account:
            _dict['userAccount'] = self.user_account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of business_account
        if self.business_account:
            _dict['businessAccount'] = self.business_account.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetUserByEmailOrUsernameV2Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "userAccount": UserAccount.from_dict(obj["userAccount"]) if obj.get("userAccount") is not None else None,
            "businessAccount": BusinessAccount.from_dict(obj["businessAccount"]) if obj.get("businessAccount") is not None else None,
            "ssoToken": obj.get("ssoToken")
        })
        return _obj


