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

from solomonai_backend_client_sdk.models.plaid_account_transaction import PlaidAccountTransaction

class TestPlaidAccountTransaction(unittest.TestCase):
    """PlaidAccountTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PlaidAccountTransaction:
        """Test PlaidAccountTransaction
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PlaidAccountTransaction`
        """
        model = PlaidAccountTransaction()
        if include_optional:
            return PlaidAccountTransaction(
                account_id = '',
                amount = 1.337,
                iso_currency_code = '',
                unofficial_currency_code = '',
                transaction_id = '',
                transaction_code = '',
                current_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                current_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                authorized_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                authorized_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                category_id = '',
                categories = [
                    ''
                    ],
                personal_finance_category_primary = '',
                personal_finance_category_detailed = '',
                transaction_name = '',
                merchant_name = '',
                check_number = '',
                payment_channel = '',
                pending = True,
                pending_transaction_id = '',
                account_owner = '',
                payment_meta_by_order_of = '',
                payment_meta_payee = '',
                payment_meta_payer = '',
                payment_meta_payment_method = '',
                payment_meta_payment_processor = '',
                payment_meta_ppd_id = '',
                payment_meta_reason = '',
                payment_meta_reference_number = '',
                location_address = '',
                location_city = '',
                location_region = '',
                location_postal_code = '',
                location_country = '',
                location_lat = 1.337,
                location_lon = 1.337,
                location_store_number = '',
                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                additional_properties = {
                    'key' : null
                    },
                id = '',
                user_id = '',
                link_id = '',
                needs_review = True,
                hide_transaction = True,
                tags = [
                    ''
                    ],
                notes = [
                    solomonai_backend_client_sdk.models.note_schema.Note schema(
                        id = '', 
                        user_id = '', 
                        content = 'Note content here...', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                splits = [
                    solomonai_backend_client_sdk.models.transaction_split.TransactionSplit(
                        id = '', 
                        user_id = '', 
                        link_id = '', 
                        description = '', 
                        amount = 1.337, 
                        categories = [
                            ''
                            ], 
                        personal_finance_category_primary = '', 
                        personal_finance_category_detailed = '', 
                        tags = [
                            ''
                            ], 
                        authorized_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        authorized_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        time_of_split = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        gl_code = '', 
                        cost_center = '', 
                        project_code = '', 
                        tax_amount = 1.337, 
                        tax_rate = 1.337, 
                        tax_code = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        created_by_email = '', )
                    ],
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                cost_center = '',
                project = '',
                tax_amount = 1.337,
                tax_rate = 1.337,
                tax_code = '',
                tax_jurisdiction = '',
                tax_type = '',
                invoice_number = '',
                billing_reference = '',
                payment_terms = '',
                vendor_id = '',
                vendor_name = '',
                customer_name = '',
                approval_status = 'APPROVAL_STATUS_UNSPECIFIED',
                approved_by_email = '',
                approved_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                transaction_status = 'TRANSACTION_STATUS_UNSPECIFIED',
                attachments = [
                    solomonai_backend_client_sdk.models.attachment.Attachment(
                        id = '', 
                        file_name = '', 
                        file_type = '', 
                        file_url = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                is_recurring = True,
                recurring_frequency = 'RECURRING_FREQUENCY_UNSPECIFIED',
                exchange_rate = 1.337,
                base_currency_amount = 1.337,
                enable_regulatory_compliance = True,
                regulatory_compliance_status = 'REGULATORY_COMPLIANCE_STATUS_UNSPECIFIED',
                payment_id = '',
                settlement_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                risk_score = 1.337,
                risk_flags = [
                    ''
                    ],
                sox_compliant = True,
                gdpr_compliant = True,
                assigned_to_user_id = ''
            )
        else:
            return PlaidAccountTransaction(
        )
        """

    def testPlaidAccountTransaction(self):
        """Test PlaidAccountTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
