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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from solomonai_backend_client_sdk.models.any import Any
from solomonai_backend_client_sdk.models.approval_status import ApprovalStatus
from solomonai_backend_client_sdk.models.attachment import Attachment
from solomonai_backend_client_sdk.models.recurring_frequency import RecurringFrequency
from solomonai_backend_client_sdk.models.regulatory_compliance_status import RegulatoryComplianceStatus
from solomonai_backend_client_sdk.models.smart_note import SmartNote
from solomonai_backend_client_sdk.models.transaction_split import TransactionSplit
from solomonai_backend_client_sdk.models.transaction_status import TransactionStatus
from typing import Optional, Set
from typing_extensions import Self

class PlaidAccountTransaction(BaseModel):
    """
    Message representing Plaid account transactions.
    """ # noqa: E501
    account_id: Optional[StrictStr] = Field(default=None, description="The bank account ID associated with the transaction.", alias="accountId")
    amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The amount of the transaction.  @gotag: ch:\"amount\"")
    iso_currency_code: Optional[StrictStr] = Field(default=None, description="The currency code of the transaction.  @gotag: ch:\"iso_currency_code\"", alias="isoCurrencyCode")
    unofficial_currency_code: Optional[StrictStr] = Field(default=None, description="The unofficial currency code of the transaction.  @gotag: ch:\"unofficial_currency_code\"", alias="unofficialCurrencyCode")
    transaction_id: Optional[StrictStr] = Field(default=None, description="The transaction ID of interest.  @gotag: ch:\"transaction_id\"", alias="transactionId")
    transaction_code: Optional[StrictStr] = Field(default=None, description="The transaction code.  @gotag: ch:\"transaction_code\"", alias="transactionCode")
    current_date: Optional[datetime] = Field(default=None, description="The date of the transaction.  @gotag: ch:\"date\"", alias="currentDate")
    current_datetime: Optional[datetime] = Field(default=None, description="The current datetime of the transaction.  @gotag: ch:\"datetime\"", alias="currentDatetime")
    authorized_date: Optional[datetime] = Field(default=None, description="The time at which the transaction was authorized.  @gotag: ch:\"authorized_date\"", alias="authorizedDate")
    authorized_datetime: Optional[datetime] = Field(default=None, description="The date-time when the transaction was authorized.  @gotag: ch:\"authorized_datetime\"", alias="authorizedDatetime")
    category_id: Optional[StrictStr] = Field(default=None, description="The category ID of the transaction.  @gotag: ch:\"category_id\"", alias="categoryId")
    categories: Optional[List[StrictStr]] = Field(default=None, description="The set of categories that the transaction belongs to.")
    personal_finance_category_primary: Optional[StrictStr] = Field(default=None, description="The primary personal finance category of the transaction.  @gotag: ch:\"personal_finance_category_primary\"", alias="personalFinanceCategoryPrimary")
    personal_finance_category_detailed: Optional[StrictStr] = Field(default=None, description="The detailed personal finance category of the transaction.  @gotag: ch:\"personal_finance_category_detailed\"", alias="personalFinanceCategoryDetailed")
    transaction_name: Optional[StrictStr] = Field(default=None, description="The name of the transaction.  @gotag: ch:\"name\"", alias="transactionName")
    merchant_name: Optional[StrictStr] = Field(default=None, description="The merchant name of the transaction.  @gotag: ch:\"merchant_name\"", alias="merchantName")
    check_number: Optional[StrictStr] = Field(default=None, description="The check number associated with the transaction.  @gotag: ch:\"check_number\"", alias="checkNumber")
    payment_channel: Optional[StrictStr] = Field(default=None, description="The payment channel for the transaction.  @gotag: ch:\"payment_channel\"", alias="paymentChannel")
    pending: Optional[StrictBool] = Field(default=None, description="Indicates whether the transaction is pending.  @gotag: ch:\"pending\"")
    pending_transaction_id: Optional[StrictStr] = Field(default=None, description="The ID of the pending transaction, if applicable.  @gotag: ch:\"pending_transaction_id\"", alias="pendingTransactionId")
    account_owner: Optional[StrictStr] = Field(default=None, description="The account owner associated with the transaction.  @gotag: ch:\"account_owner\"", alias="accountOwner")
    payment_meta_by_order_of: Optional[StrictStr] = Field(default=None, description="Information about the entity to whom the payment is made (if available).", alias="paymentMetaByOrderOf")
    payment_meta_payee: Optional[StrictStr] = Field(default=None, description="Information about the payee (if available).", alias="paymentMetaPayee")
    payment_meta_payer: Optional[StrictStr] = Field(default=None, description="Information about the payer (if available).", alias="paymentMetaPayer")
    payment_meta_payment_method: Optional[StrictStr] = Field(default=None, description="The payment method used for the transaction (if available).", alias="paymentMetaPaymentMethod")
    payment_meta_payment_processor: Optional[StrictStr] = Field(default=None, description="The payment processor involved in the transaction (if available).", alias="paymentMetaPaymentProcessor")
    payment_meta_ppd_id: Optional[StrictStr] = Field(default=None, description="The Prearranged Payment and Deposit (PPD) ID (if available).", alias="paymentMetaPpdId")
    payment_meta_reason: Optional[StrictStr] = Field(default=None, description="The reason for the payment (if available).", alias="paymentMetaReason")
    payment_meta_reference_number: Optional[StrictStr] = Field(default=None, description="The reference number associated with the payment (if available).", alias="paymentMetaReferenceNumber")
    location_address: Optional[StrictStr] = Field(default=None, description="The street address of the transaction location (if available).", alias="locationAddress")
    location_city: Optional[StrictStr] = Field(default=None, description="The city of the transaction location (if available).", alias="locationCity")
    location_region: Optional[StrictStr] = Field(default=None, description="The region or state of the transaction location (if available).", alias="locationRegion")
    location_postal_code: Optional[StrictStr] = Field(default=None, description="The postal code of the transaction location (if available).", alias="locationPostalCode")
    location_country: Optional[StrictStr] = Field(default=None, description="The country of the transaction location (if available).", alias="locationCountry")
    location_lat: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The latitude of the transaction location (if available).", alias="locationLat")
    location_lon: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The longitude of the transaction location (if available).", alias="locationLon")
    location_store_number: Optional[StrictStr] = Field(default=None, description="The store number associated with the transaction location (if available).", alias="locationStoreNumber")
    time: Optional[datetime] = Field(default=None, description="The timestamp associated with the transaction.")
    additional_properties: Optional[Any] = Field(default=None, alias="additionalProperties")
    id: Optional[StrictStr] = Field(default=None, description="The unique ID for this transaction.")
    user_id: Optional[StrictStr] = Field(default=None, description="The user ID associated with this transaction.", alias="userId")
    link_id: Optional[StrictStr] = Field(default=None, description="The link ID associated with this transaction.", alias="linkId")
    needs_review: Optional[StrictBool] = Field(default=None, description="Indicates whether this transaction needs review.", alias="needsReview")
    hide_transaction: Optional[StrictBool] = Field(default=None, description="Indicates whether this transaction should be hidden.", alias="hideTransaction")
    tags: Optional[List[StrictStr]] = Field(default=None, description="Tags associated with this transaction.")
    notes: Optional[List[SmartNote]] = Field(default=None, description="Notes associated with this transaction.")
    splits: Optional[List[TransactionSplit]] = Field(default=None, description="The number of splits associated with this transaction.")
    deleted_at: Optional[datetime] = Field(default=None, alias="deletedAt")
    cost_center: Optional[StrictStr] = Field(default=None, description="The cost center associated with this transaction.", alias="costCenter")
    project: Optional[StrictStr] = Field(default=None, description="The project associated with this transaction.")
    tax_amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The tax amount associated with this transaction.", alias="taxAmount")
    tax_rate: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The tax rate applied to this transaction.", alias="taxRate")
    tax_code: Optional[StrictStr] = Field(default=None, description="The tax code associated with this transaction.", alias="taxCode")
    tax_jurisdiction: Optional[StrictStr] = Field(default=None, description="The tax jurisdiction.", alias="taxJurisdiction")
    tax_type: Optional[StrictStr] = Field(default=None, description="The type of tax (e.g., VAT, GST, Sales Tax).", alias="taxType")
    invoice_number: Optional[StrictStr] = Field(default=None, description="The invoice number associated with this transaction.", alias="invoiceNumber")
    billing_reference: Optional[StrictStr] = Field(default=None, alias="billingReference")
    payment_terms: Optional[StrictStr] = Field(default=None, description="The payment terms associated with this transaction.", alias="paymentTerms")
    vendor_id: Optional[StrictStr] = Field(default=None, description="The vendor ID associated with this transaction.", alias="vendorId")
    vendor_name: Optional[StrictStr] = Field(default=None, description="The vendor name associated with this transaction.", alias="vendorName")
    customer_name: Optional[StrictStr] = Field(default=None, description="The customer name associated with this transaction.", alias="customerName")
    approval_status: Optional[ApprovalStatus] = Field(default=ApprovalStatus.UNSPECIFIED, alias="approvalStatus")
    approved_by_email: Optional[StrictStr] = Field(default=None, description="The email of the user who approved this transaction.", alias="approvedByEmail")
    approved_date: Optional[datetime] = Field(default=None, description="The date when this transaction was approved.", alias="approvedDate")
    transaction_status: Optional[TransactionStatus] = Field(default=TransactionStatus.UNSPECIFIED, alias="transactionStatus")
    attachments: Optional[List[Attachment]] = Field(default=None, description="The attachments associated with this transaction.")
    is_recurring: Optional[StrictBool] = Field(default=None, description="Indicates whether this transaction is recurring.", alias="isRecurring")
    recurring_frequency: Optional[RecurringFrequency] = Field(default=RecurringFrequency.UNSPECIFIED, alias="recurringFrequency")
    exchange_rate: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The exchange rate applied to this transaction.", alias="exchangeRate")
    base_currency_amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The base currency amount of the transaction.", alias="baseCurrencyAmount")
    enable_regulatory_compliance: Optional[StrictBool] = Field(default=None, description="Indicates whether this transaction is enabled for regulatory compliance.", alias="enableRegulatoryCompliance")
    regulatory_compliance_status: Optional[RegulatoryComplianceStatus] = Field(default=RegulatoryComplianceStatus.UNSPECIFIED, alias="regulatoryComplianceStatus")
    payment_id: Optional[StrictStr] = Field(default=None, description="The payment ID associated with this transaction.", alias="paymentId")
    settlement_date: Optional[datetime] = Field(default=None, description="The settlement date of the transaction.", alias="settlementDate")
    risk_score: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The risk score of the transaction.", alias="riskScore")
    risk_flags: Optional[List[StrictStr]] = Field(default=None, description="The risk flags of the transaction.", alias="riskFlags")
    sox_compliant: Optional[StrictBool] = Field(default=None, description="Indicates whether this transaction is subject to SOX compliance.", alias="soxCompliant")
    gdpr_compliant: Optional[StrictBool] = Field(default=None, description="Indicates whether this transaction is subject to GDPR compliance.", alias="gdprCompliant")
    assigned_to_user_id: Optional[StrictStr] = Field(default=None, description="The email of the user assigned to this transaction.", alias="assignedToUserId")
    __properties: ClassVar[List[str]] = ["accountId", "amount", "isoCurrencyCode", "unofficialCurrencyCode", "transactionId", "transactionCode", "currentDate", "currentDatetime", "authorizedDate", "authorizedDatetime", "categoryId", "categories", "personalFinanceCategoryPrimary", "personalFinanceCategoryDetailed", "transactionName", "merchantName", "checkNumber", "paymentChannel", "pending", "pendingTransactionId", "accountOwner", "paymentMetaByOrderOf", "paymentMetaPayee", "paymentMetaPayer", "paymentMetaPaymentMethod", "paymentMetaPaymentProcessor", "paymentMetaPpdId", "paymentMetaReason", "paymentMetaReferenceNumber", "locationAddress", "locationCity", "locationRegion", "locationPostalCode", "locationCountry", "locationLat", "locationLon", "locationStoreNumber", "time", "additionalProperties", "id", "userId", "linkId", "needsReview", "hideTransaction", "tags", "notes", "splits", "deletedAt", "costCenter", "project", "taxAmount", "taxRate", "taxCode", "taxJurisdiction", "taxType", "invoiceNumber", "billingReference", "paymentTerms", "vendorId", "vendorName", "customerName", "approvalStatus", "approvedByEmail", "approvedDate", "transactionStatus", "attachments", "isRecurring", "recurringFrequency", "exchangeRate", "baseCurrencyAmount", "enableRegulatoryCompliance", "regulatoryComplianceStatus", "paymentId", "settlementDate", "riskScore", "riskFlags", "soxCompliant", "gdprCompliant", "assignedToUserId"]

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
        """Create an instance of PlaidAccountTransaction from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of additional_properties
        if self.additional_properties:
            _dict['additionalProperties'] = self.additional_properties.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in notes (list)
        _items = []
        if self.notes:
            for _item in self.notes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['notes'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in splits (list)
        _items = []
        if self.splits:
            for _item in self.splits:
                if _item:
                    _items.append(_item.to_dict())
            _dict['splits'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in attachments (list)
        _items = []
        if self.attachments:
            for _item in self.attachments:
                if _item:
                    _items.append(_item.to_dict())
            _dict['attachments'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PlaidAccountTransaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "accountId": obj.get("accountId"),
            "amount": obj.get("amount"),
            "isoCurrencyCode": obj.get("isoCurrencyCode"),
            "unofficialCurrencyCode": obj.get("unofficialCurrencyCode"),
            "transactionId": obj.get("transactionId"),
            "transactionCode": obj.get("transactionCode"),
            "currentDate": obj.get("currentDate"),
            "currentDatetime": obj.get("currentDatetime"),
            "authorizedDate": obj.get("authorizedDate"),
            "authorizedDatetime": obj.get("authorizedDatetime"),
            "categoryId": obj.get("categoryId"),
            "categories": obj.get("categories"),
            "personalFinanceCategoryPrimary": obj.get("personalFinanceCategoryPrimary"),
            "personalFinanceCategoryDetailed": obj.get("personalFinanceCategoryDetailed"),
            "transactionName": obj.get("transactionName"),
            "merchantName": obj.get("merchantName"),
            "checkNumber": obj.get("checkNumber"),
            "paymentChannel": obj.get("paymentChannel"),
            "pending": obj.get("pending"),
            "pendingTransactionId": obj.get("pendingTransactionId"),
            "accountOwner": obj.get("accountOwner"),
            "paymentMetaByOrderOf": obj.get("paymentMetaByOrderOf"),
            "paymentMetaPayee": obj.get("paymentMetaPayee"),
            "paymentMetaPayer": obj.get("paymentMetaPayer"),
            "paymentMetaPaymentMethod": obj.get("paymentMetaPaymentMethod"),
            "paymentMetaPaymentProcessor": obj.get("paymentMetaPaymentProcessor"),
            "paymentMetaPpdId": obj.get("paymentMetaPpdId"),
            "paymentMetaReason": obj.get("paymentMetaReason"),
            "paymentMetaReferenceNumber": obj.get("paymentMetaReferenceNumber"),
            "locationAddress": obj.get("locationAddress"),
            "locationCity": obj.get("locationCity"),
            "locationRegion": obj.get("locationRegion"),
            "locationPostalCode": obj.get("locationPostalCode"),
            "locationCountry": obj.get("locationCountry"),
            "locationLat": obj.get("locationLat"),
            "locationLon": obj.get("locationLon"),
            "locationStoreNumber": obj.get("locationStoreNumber"),
            "time": obj.get("time"),
            "additionalProperties": Any.from_dict(obj["additionalProperties"]) if obj.get("additionalProperties") is not None else None,
            "id": obj.get("id"),
            "userId": obj.get("userId"),
            "linkId": obj.get("linkId"),
            "needsReview": obj.get("needsReview"),
            "hideTransaction": obj.get("hideTransaction"),
            "tags": obj.get("tags"),
            "notes": [SmartNote.from_dict(_item) for _item in obj["notes"]] if obj.get("notes") is not None else None,
            "splits": [TransactionSplit.from_dict(_item) for _item in obj["splits"]] if obj.get("splits") is not None else None,
            "deletedAt": obj.get("deletedAt"),
            "costCenter": obj.get("costCenter"),
            "project": obj.get("project"),
            "taxAmount": obj.get("taxAmount"),
            "taxRate": obj.get("taxRate"),
            "taxCode": obj.get("taxCode"),
            "taxJurisdiction": obj.get("taxJurisdiction"),
            "taxType": obj.get("taxType"),
            "invoiceNumber": obj.get("invoiceNumber"),
            "billingReference": obj.get("billingReference"),
            "paymentTerms": obj.get("paymentTerms"),
            "vendorId": obj.get("vendorId"),
            "vendorName": obj.get("vendorName"),
            "customerName": obj.get("customerName"),
            "approvalStatus": obj.get("approvalStatus") if obj.get("approvalStatus") is not None else ApprovalStatus.UNSPECIFIED,
            "approvedByEmail": obj.get("approvedByEmail"),
            "approvedDate": obj.get("approvedDate"),
            "transactionStatus": obj.get("transactionStatus") if obj.get("transactionStatus") is not None else TransactionStatus.UNSPECIFIED,
            "attachments": [Attachment.from_dict(_item) for _item in obj["attachments"]] if obj.get("attachments") is not None else None,
            "isRecurring": obj.get("isRecurring"),
            "recurringFrequency": obj.get("recurringFrequency") if obj.get("recurringFrequency") is not None else RecurringFrequency.UNSPECIFIED,
            "exchangeRate": obj.get("exchangeRate"),
            "baseCurrencyAmount": obj.get("baseCurrencyAmount"),
            "enableRegulatoryCompliance": obj.get("enableRegulatoryCompliance"),
            "regulatoryComplianceStatus": obj.get("regulatoryComplianceStatus") if obj.get("regulatoryComplianceStatus") is not None else RegulatoryComplianceStatus.UNSPECIFIED,
            "paymentId": obj.get("paymentId"),
            "settlementDate": obj.get("settlementDate"),
            "riskScore": obj.get("riskScore"),
            "riskFlags": obj.get("riskFlags"),
            "soxCompliant": obj.get("soxCompliant"),
            "gdprCompliant": obj.get("gdprCompliant"),
            "assignedToUserId": obj.get("assignedToUserId")
        })
        return _obj


