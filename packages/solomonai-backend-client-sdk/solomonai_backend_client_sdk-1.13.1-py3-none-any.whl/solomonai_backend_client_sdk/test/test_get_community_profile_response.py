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

from solomonai_backend_client_sdk.models.get_community_profile_response import GetCommunityProfileResponse

class TestGetCommunityProfileResponse(unittest.TestCase):
    """GetCommunityProfileResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetCommunityProfileResponse:
        """Test GetCommunityProfileResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetCommunityProfileResponse`
        """
        model = GetCommunityProfileResponse()
        if include_optional:
            return GetCommunityProfileResponse(
                profile = solomonai_backend_client_sdk.models.community_profile:_the_profile_object_tied_to_a_given_community.CommunityProfile: The profile object tied to a given community(
                    id = '', 
                    name = 'test-community', 
                    description = 'community description useful for generating a test community that we can test against. a community is really cool and ideal', 
                    private = True, 
                    visible = True, 
                    followers = '', 
                    community_rules = 'community rules useful for generating a test community that we can test against. a community is really cool and ideal', 
                    topics = [
                        solomonai_backend_client_sdk.models.topic:_topic_that_can_be_associated_to_a_record.Topic: topic that can be associated to a record(
                            id = '', 
                            topic_name = 'test-tagname', 
                            description = 'test-description sakjlDKJGSAHGHFDHSGJHFGAHDFJKGSHAJDLgAKSGDHAS CSVDJKSADASKJHDASFDGJKJLHSAHGFJDSAHD kjskhdgfhgdhfgkhsdfdsdfdssdfsdf', 
                            image_url = 'test-tagname', )
                        ], 
                    notification_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                    personal_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                    news_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                    profile_image_url = 'asndlkhaskhdhasgdahsf.jpg', 
                    algolia_id = 'asndlkhaskhdhasgdahsf-feed-id', ),
                metadata = solomonai_backend_client_sdk.models.social_relationship_metadata.SocialRelationshipMetadata(
                    source_profile = solomonai_backend_client_sdk.models.social_profile_metadata.SocialProfileMetadata(
                        profile_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                        profile_id = '', ), 
                    target_profile = solomonai_backend_client_sdk.models.social_profile_metadata.SocialProfileMetadata(
                        profile_id = '', ), 
                    following = True, 
                    following_since = '', )
            )
        else:
            return GetCommunityProfileResponse(
        )
        """

    def testGetCommunityProfileResponse(self):
        """Test GetCommunityProfileResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
