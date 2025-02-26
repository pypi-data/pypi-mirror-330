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

from solomonai_backend_client_sdk.models.business_transaction import BusinessTransaction

class TestBusinessTransaction(unittest.TestCase):
    """BusinessTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BusinessTransaction:
        """Test BusinessTransaction
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BusinessTransaction`
        """
        model = BusinessTransaction()
        if include_optional:
            return BusinessTransaction(
                id = '',
                transaction_type = '',
                number = '',
                transaction_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                account = '',
                contact = '',
                total_amount = '',
                currency = '',
                exchange_rate = '',
                company = '',
                tracking_categories = [
                    ''
                    ],
                line_items = [
                    solomonai_backend_client_sdk.models.transaction_line_item.TransactionLineItem(
                        id = '', 
                        remote_id = '', 
                        memo = '', 
                        unit_price = '', 
                        quantity = '', 
                        item = '', 
                        account = '', 
                        tracking_category = '', 
                        tracking_categories = [
                            ''
                            ], 
                        total_line_amount = '', 
                        tax_rate = '', 
                        currency = '', 
                        exchange_rate = '', 
                        company = '', 
                        modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        remote_was_deleted = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                remote_was_deleted = True,
                accounting_period = '',
                merge_record_id = '',
                remote_id = '',
                modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return BusinessTransaction(
        )
        """

    def testBusinessTransaction(self):
        """Test BusinessTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
