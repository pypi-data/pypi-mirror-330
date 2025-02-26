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

from solomonai_backend_client_sdk.models.social_relationship_metadata import SocialRelationshipMetadata

class TestSocialRelationshipMetadata(unittest.TestCase):
    """SocialRelationshipMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SocialRelationshipMetadata:
        """Test SocialRelationshipMetadata
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SocialRelationshipMetadata`
        """
        model = SocialRelationshipMetadata()
        if include_optional:
            return SocialRelationshipMetadata(
                source_profile = solomonai_backend_client_sdk.models.social_profile_metadata.SocialProfileMetadata(
                    profile_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                    profile_id = '', ),
                target_profile = solomonai_backend_client_sdk.models.social_profile_metadata.SocialProfileMetadata(
                    profile_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                    profile_id = '', ),
                following = True,
                following_since = ''
            )
        else:
            return SocialRelationshipMetadata(
                source_profile = solomonai_backend_client_sdk.models.social_profile_metadata.SocialProfileMetadata(
                    profile_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                    profile_id = '', ),
                target_profile = solomonai_backend_client_sdk.models.social_profile_metadata.SocialProfileMetadata(
                    profile_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                    profile_id = '', ),
        )
        """

    def testSocialRelationshipMetadata(self):
        """Test SocialRelationshipMetadata"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
