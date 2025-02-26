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

from solomonai_backend_client_sdk.models.delete_community_profile_response import DeleteCommunityProfileResponse

class TestDeleteCommunityProfileResponse(unittest.TestCase):
    """DeleteCommunityProfileResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DeleteCommunityProfileResponse:
        """Test DeleteCommunityProfileResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DeleteCommunityProfileResponse`
        """
        model = DeleteCommunityProfileResponse()
        if include_optional:
            return DeleteCommunityProfileResponse(
                success = True
            )
        else:
            return DeleteCommunityProfileResponse(
        )
        """

    def testDeleteCommunityProfileResponse(self):
        """Test DeleteCommunityProfileResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
