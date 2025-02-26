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

from solomonai_backend_client_sdk.models.company_info import CompanyInfo

class TestCompanyInfo(unittest.TestCase):
    """CompanyInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CompanyInfo:
        """Test CompanyInfo
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CompanyInfo`
        """
        model = CompanyInfo()
        if include_optional:
            return CompanyInfo(
                id = '',
                remote_id = '',
                name = '',
                legal_name = '',
                tax_number = '',
                fiscal_year_end_month = 56,
                fiscal_year_end_day = 56,
                currency = '',
                remote_created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                urls = [
                    ''
                    ],
                addresses = [
                    solomonai_backend_client_sdk.models.company_address.CompanyAddress(
                        id = '', 
                        type = '', 
                        street1 = '', 
                        street2 = '', 
                        city = '', 
                        state = '', 
                        country_subdivision = '', 
                        country = '', 
                        zip_code = '', 
                        modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                phone_numbers = [
                    ''
                    ],
                remote_was_deleted = True,
                modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                merge_record_id = '',
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return CompanyInfo(
        )
        """

    def testCompanyInfo(self):
        """Test CompanyInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
