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

from solomonai_backend_client_sdk.models.plaid_initiate_token_update_request import PlaidInitiateTokenUpdateRequest

class TestPlaidInitiateTokenUpdateRequest(unittest.TestCase):
    """PlaidInitiateTokenUpdateRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PlaidInitiateTokenUpdateRequest:
        """Test PlaidInitiateTokenUpdateRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PlaidInitiateTokenUpdateRequest`
        """
        model = PlaidInitiateTokenUpdateRequest()
        if include_optional:
            return PlaidInitiateTokenUpdateRequest(
                user_id = '',
                link_id = '',
                profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED',
                org_id = 'org_12345',
                tenant_id = 'tenant_67890'
            )
        else:
            return PlaidInitiateTokenUpdateRequest(
                user_id = '',
                link_id = '',
                profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED',
                org_id = 'org_12345',
                tenant_id = 'tenant_67890',
        )
        """

    def testPlaidInitiateTokenUpdateRequest(self):
        """Test PlaidInitiateTokenUpdateRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
