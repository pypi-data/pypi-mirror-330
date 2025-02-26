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

from solomonai_backend_client_sdk.models.get_location_metrics_financial_sub_profile_over_time_response import GetLocationMetricsFinancialSubProfileOverTimeResponse

class TestGetLocationMetricsFinancialSubProfileOverTimeResponse(unittest.TestCase):
    """GetLocationMetricsFinancialSubProfileOverTimeResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetLocationMetricsFinancialSubProfileOverTimeResponse:
        """Test GetLocationMetricsFinancialSubProfileOverTimeResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetLocationMetricsFinancialSubProfileOverTimeResponse`
        """
        model = GetLocationMetricsFinancialSubProfileOverTimeResponse()
        if include_optional:
            return GetLocationMetricsFinancialSubProfileOverTimeResponse(
                data = [
                    solomonai_backend_client_sdk.models.location_financial_sub_profile.LocationFinancialSubProfile(
                        location_city = '', 
                        transaction_count = '', 
                        spent_last_week = 1.337, 
                        spent_last_two_weeks = 1.337, 
                        spent_last_month = 1.337, 
                        spent_last_six_months = 1.337, 
                        spent_last_year = 1.337, 
                        spent_last_two_years = 1.337, 
                        user_id = '', 
                        month = 56, 
                        profile_type = 'FINANCIAL_USER_PROFILE_TYPE_UNSPECIFIED', )
                    ]
            )
        else:
            return GetLocationMetricsFinancialSubProfileOverTimeResponse(
        )
        """

    def testGetLocationMetricsFinancialSubProfileOverTimeResponse(self):
        """Test GetLocationMetricsFinancialSubProfileOverTimeResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
