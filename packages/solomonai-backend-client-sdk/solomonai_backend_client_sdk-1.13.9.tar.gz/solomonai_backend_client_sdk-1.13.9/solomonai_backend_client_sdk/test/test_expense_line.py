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

from solomonai_backend_client_sdk.models.expense_line import ExpenseLine

class TestExpenseLine(unittest.TestCase):
    """ExpenseLine unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ExpenseLine:
        """Test ExpenseLine
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ExpenseLine`
        """
        model = ExpenseLine()
        if include_optional:
            return ExpenseLine(
                id = '',
                net_amount = 1.337,
                tracking_category = '',
                tracking_categories = [
                    ''
                    ],
                company = '',
                item = '',
                account = '',
                contact = '',
                description = '',
                exchange_rate = '',
                remote_id = '',
                currency = '',
                modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                remote_was_deleted = True,
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return ExpenseLine(
        )
        """

    def testExpenseLine(self):
        """Test ExpenseLine"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
