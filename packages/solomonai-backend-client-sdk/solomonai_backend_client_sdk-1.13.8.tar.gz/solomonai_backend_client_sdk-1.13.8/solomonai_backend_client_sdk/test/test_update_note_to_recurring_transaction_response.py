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

from solomonai_backend_client_sdk.models.update_note_to_recurring_transaction_response import UpdateNoteToRecurringTransactionResponse

class TestUpdateNoteToRecurringTransactionResponse(unittest.TestCase):
    """UpdateNoteToRecurringTransactionResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateNoteToRecurringTransactionResponse:
        """Test UpdateNoteToRecurringTransactionResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateNoteToRecurringTransactionResponse`
        """
        model = UpdateNoteToRecurringTransactionResponse()
        if include_optional:
            return UpdateNoteToRecurringTransactionResponse(
                transaction = solomonai_backend_client_sdk.models.plaid_account_recurring_transaction.PlaidAccountRecurringTransaction(
                    account_id = '', 
                    stream_id = '', 
                    category_id = '', 
                    description = '', 
                    merchant_name = '', 
                    personal_finance_category_primary = '', 
                    personal_finance_category_detailed = '', 
                    first_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    last_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    frequency = '', 
                    transaction_ids = '', 
                    average_amount = '', 
                    average_amount_iso_currency_code = '', 
                    last_amount = '', 
                    last_amount_iso_currency_code = '', 
                    is_active = True, 
                    status = '', 
                    updated_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    user_id = '', 
                    link_id = '', 
                    id = '', 
                    flow = '', 
                    time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    additional_properties = {
                        'key' : null
                        }, 
                    notes = [
                        solomonai_backend_client_sdk.models.note_schema.Note schema(
                            id = '', 
                            user_id = '', 
                            content = 'Note content here...', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return UpdateNoteToRecurringTransactionResponse(
        )
        """

    def testUpdateNoteToRecurringTransactionResponse(self):
        """Test UpdateNoteToRecurringTransactionResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
