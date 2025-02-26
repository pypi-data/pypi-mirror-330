# coding: utf-8

"""
    User Service API

    Solomon AI User Service API - Manages user profiles and authentication

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@solomon-ai.co
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from solomonai_backend_client_sdk.models.plaid_sync_account_from_access_token_request import PlaidSyncAccountFromAccessTokenRequest

class TestPlaidSyncAccountFromAccessTokenRequest(unittest.TestCase):
    """PlaidSyncAccountFromAccessTokenRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PlaidSyncAccountFromAccessTokenRequest:
        """Test PlaidSyncAccountFromAccessTokenRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PlaidSyncAccountFromAccessTokenRequest`
        """
        model = PlaidSyncAccountFromAccessTokenRequest()
        if include_optional:
            return PlaidSyncAccountFromAccessTokenRequest(
                user_id = '',
                access_token = '',
                institution_id = '',
                institution_name = '',
                profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED',
                item_id = '',
                org_id = 'org_12345',
                tenant_id = 'tenant_67890'
            )
        else:
            return PlaidSyncAccountFromAccessTokenRequest(
                user_id = '',
                access_token = '',
                profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED',
                org_id = 'org_12345',
                tenant_id = 'tenant_67890',
        )
        """

    def testPlaidSyncAccountFromAccessTokenRequest(self):
        """Test PlaidSyncAccountFromAccessTokenRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
