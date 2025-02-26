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

from solomonai_backend_client_sdk.models.create_account_request import CreateAccountRequest

class TestCreateAccountRequest(unittest.TestCase):
    """CreateAccountRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateAccountRequest:
        """Test CreateAccountRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateAccountRequest`
        """
        model = CreateAccountRequest()
        if include_optional:
            return CreateAccountRequest(
                user_id = '',
                email = '',
                metadata = {
                    'key' : ''
                    },
                org_id = '',
                tenant_id = ''
            )
        else:
            return CreateAccountRequest(
                user_id = '',
                email = '',
                org_id = '',
                tenant_id = '',
        )
        """

    def testCreateAccountRequest(self):
        """Test CreateAccountRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
