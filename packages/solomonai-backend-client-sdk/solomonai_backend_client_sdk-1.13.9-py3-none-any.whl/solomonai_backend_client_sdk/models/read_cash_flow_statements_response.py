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

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from solomonai_backend_client_sdk.models.cash_flow_statement import CashFlowStatement
from typing import Optional, Set
from typing_extensions import Self

class ReadCashFlowStatementsResponse(BaseModel):
    """
    ReadCashFlowStatementsResponse
    """ # noqa: E501
    cash_flow_statements: Optional[List[CashFlowStatement]] = Field(default=None, alias="cashFlowStatements")
    next_page: Optional[StrictInt] = Field(default=None, alias="nextPage")
    __properties: ClassVar[List[str]] = ["cashFlowStatements", "nextPage"]

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
        """Create an instance of ReadCashFlowStatementsResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in cash_flow_statements (list)
        _items = []
        if self.cash_flow_statements:
            for _item in self.cash_flow_statements:
                if _item:
                    _items.append(_item.to_dict())
            _dict['cashFlowStatements'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ReadCashFlowStatementsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "cashFlowStatements": [CashFlowStatement.from_dict(_item) for _item in obj["cashFlowStatements"]] if obj.get("cashFlowStatements") is not None else None,
            "nextPage": obj.get("nextPage")
        })
        return _obj


