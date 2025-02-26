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

from solomonai_backend_client_sdk.models.get_user_category_monthly_income_response import GetUserCategoryMonthlyIncomeResponse

class TestGetUserCategoryMonthlyIncomeResponse(unittest.TestCase):
    """GetUserCategoryMonthlyIncomeResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetUserCategoryMonthlyIncomeResponse:
        """Test GetUserCategoryMonthlyIncomeResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetUserCategoryMonthlyIncomeResponse`
        """
        model = GetUserCategoryMonthlyIncomeResponse()
        if include_optional:
            return GetUserCategoryMonthlyIncomeResponse(
                category_monthly_income = [
                    solomonai_backend_client_sdk.models.category_monthly_income.CategoryMonthlyIncome(
                        month = 56, 
                        personal_finance_category_primary = '', 
                        total_income = 1.337, 
                        user_id = '', 
                        profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED', )
                    ],
                next_page_number = ''
            )
        else:
            return GetUserCategoryMonthlyIncomeResponse(
        )
        """

    def testGetUserCategoryMonthlyIncomeResponse(self):
        """Test GetUserCategoryMonthlyIncomeResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
