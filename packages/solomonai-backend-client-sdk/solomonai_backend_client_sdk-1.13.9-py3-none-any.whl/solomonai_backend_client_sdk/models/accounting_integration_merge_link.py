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
from solomonai_backend_client_sdk.models.linked_accounting_account import LinkedAccountingAccount
from solomonai_backend_client_sdk.models.merge_linked_account_token import MergeLinkedAccountToken
from typing import Optional, Set
from typing_extensions import Self

class AccountingIntegrationMergeLink(BaseModel):
    """
    AccountingIntegrationMergeLink
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the merge link.")
    integration: Optional[StrictStr] = Field(default=None, description="The integration name.")
    integration_slug: Optional[StrictStr] = Field(default=None, description="The slug for the integration.", alias="integrationSlug")
    category: Optional[StrictStr] = Field(default=None, description="The category of the integration.")
    end_user_origin_id: Optional[StrictStr] = Field(default=None, description="Identifier of the end user's origin.", alias="endUserOriginId")
    end_user_organization_name: Optional[StrictStr] = Field(default=None, description="Name of the end user's organization.", alias="endUserOrganizationName")
    end_user_email_address: Optional[StrictStr] = Field(default=None, description="Email address of the end user.", alias="endUserEmailAddress")
    status: Optional[StrictStr] = Field(default=None, description="Status of the merge link.")
    webhook_listener_url: Optional[StrictStr] = Field(default=None, description="URL for the webhook listener associated with the merge link.", alias="webhookListenerUrl")
    is_duplicate: Optional[StrictBool] = Field(default=None, description="Indicates whether the merge link is a duplicate.", alias="isDuplicate")
    token: Optional[MergeLinkedAccountToken] = None
    integration_name: Optional[StrictStr] = Field(default=None, description="Name of the integration.", alias="integrationName")
    integration_image: Optional[StrictStr] = Field(default=None, description="URL of the integration's image.", alias="integrationImage")
    integration_square_image: Optional[StrictStr] = Field(default=None, description="URL of the integration's square image.", alias="integrationSquareImage")
    account: Optional[LinkedAccountingAccount] = None
    merge_linked_account_id: Optional[StrictStr] = Field(default=None, description="Identifier of the merged linked account.", alias="mergeLinkedAccountId")
    last_modified_at: Optional[datetime] = Field(default=None, description="Timestamp indicating when the merge link was last modified.", alias="lastModifiedAt")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    __properties: ClassVar[List[str]] = ["id", "integration", "integrationSlug", "category", "endUserOriginId", "endUserOrganizationName", "endUserEmailAddress", "status", "webhookListenerUrl", "isDuplicate", "token", "integrationName", "integrationImage", "integrationSquareImage", "account", "mergeLinkedAccountId", "lastModifiedAt", "deletedAt", "createdAt"]

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
        """Create an instance of AccountingIntegrationMergeLink from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of token
        if self.token:
            _dict['token'] = self.token.to_dict()
        # override the default output from pydantic by calling `to_dict()` of account
        if self.account:
            _dict['account'] = self.account.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccountingIntegrationMergeLink from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "integration": obj.get("integration"),
            "integrationSlug": obj.get("integrationSlug"),
            "category": obj.get("category"),
            "endUserOriginId": obj.get("endUserOriginId"),
            "endUserOrganizationName": obj.get("endUserOrganizationName"),
            "endUserEmailAddress": obj.get("endUserEmailAddress"),
            "status": obj.get("status"),
            "webhookListenerUrl": obj.get("webhookListenerUrl"),
            "isDuplicate": obj.get("isDuplicate"),
            "token": MergeLinkedAccountToken.from_dict(obj["token"]) if obj.get("token") is not None else None,
            "integrationName": obj.get("integrationName"),
            "integrationImage": obj.get("integrationImage"),
            "integrationSquareImage": obj.get("integrationSquareImage"),
            "account": LinkedAccountingAccount.from_dict(obj["account"]) if obj.get("account") is not None else None,
            "mergeLinkedAccountId": obj.get("mergeLinkedAccountId"),
            "lastModifiedAt": obj.get("lastModifiedAt"),
            "deletedAt": obj.get("deletedAt"),
            "createdAt": obj.get("createdAt")
        })
        return _obj


