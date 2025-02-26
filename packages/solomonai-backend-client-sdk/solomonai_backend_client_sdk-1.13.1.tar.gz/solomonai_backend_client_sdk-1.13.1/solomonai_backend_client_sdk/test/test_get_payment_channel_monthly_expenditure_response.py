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

from solomonai_backend_client_sdk.models.get_payment_channel_monthly_expenditure_response import GetPaymentChannelMonthlyExpenditureResponse

class TestGetPaymentChannelMonthlyExpenditureResponse(unittest.TestCase):
    """GetPaymentChannelMonthlyExpenditureResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetPaymentChannelMonthlyExpenditureResponse:
        """Test GetPaymentChannelMonthlyExpenditureResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetPaymentChannelMonthlyExpenditureResponse`
        """
        model = GetPaymentChannelMonthlyExpenditureResponse()
        if include_optional:
            return GetPaymentChannelMonthlyExpenditureResponse(
                payment_channel_monthly_expenditure = [
                    solomonai_backend_client_sdk.models.payment_channel_monthly_expenditure.PaymentChannelMonthlyExpenditure(
                        month = 56, 
                        payment_channel = '', 
                        total_spending = 1.337, 
                        user_id = '', 
                        profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED', )
                    ],
                next_page_number = ''
            )
        else:
            return GetPaymentChannelMonthlyExpenditureResponse(
        )
        """

    def testGetPaymentChannelMonthlyExpenditureResponse(self):
        """Test GetPaymentChannelMonthlyExpenditureResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
