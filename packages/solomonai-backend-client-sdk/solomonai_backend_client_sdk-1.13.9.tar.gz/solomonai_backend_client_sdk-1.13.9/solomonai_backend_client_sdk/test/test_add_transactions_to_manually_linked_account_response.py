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

from solomonai_backend_client_sdk.models.add_transactions_to_manually_linked_account_response import AddTransactionsToManuallyLinkedAccountResponse

class TestAddTransactionsToManuallyLinkedAccountResponse(unittest.TestCase):
    """AddTransactionsToManuallyLinkedAccountResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AddTransactionsToManuallyLinkedAccountResponse:
        """Test AddTransactionsToManuallyLinkedAccountResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AddTransactionsToManuallyLinkedAccountResponse`
        """
        model = AddTransactionsToManuallyLinkedAccountResponse()
        if include_optional:
            return AddTransactionsToManuallyLinkedAccountResponse(
                succes = True
            )
        else:
            return AddTransactionsToManuallyLinkedAccountResponse(
        )
        """

    def testAddTransactionsToManuallyLinkedAccountResponse(self):
        """Test AddTransactionsToManuallyLinkedAccountResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
