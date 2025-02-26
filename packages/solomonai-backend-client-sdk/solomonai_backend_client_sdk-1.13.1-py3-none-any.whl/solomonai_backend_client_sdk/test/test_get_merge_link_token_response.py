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

from solomonai_backend_client_sdk.models.get_merge_link_token_response import GetMergeLinkTokenResponse

class TestGetMergeLinkTokenResponse(unittest.TestCase):
    """GetMergeLinkTokenResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetMergeLinkTokenResponse:
        """Test GetMergeLinkTokenResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetMergeLinkTokenResponse`
        """
        model = GetMergeLinkTokenResponse()
        if include_optional:
            return GetMergeLinkTokenResponse(
                link_token = '',
                integration_name = '',
                magic_link_url = '',
                end_user_origin_id = '',
                organization_name = ''
            )
        else:
            return GetMergeLinkTokenResponse(
        )
        """

    def testGetMergeLinkTokenResponse(self):
        """Test GetMergeLinkTokenResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
