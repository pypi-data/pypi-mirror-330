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

from solomonai_backend_client_sdk.models.discover_profiles_response import DiscoverProfilesResponse

class TestDiscoverProfilesResponse(unittest.TestCase):
    """DiscoverProfilesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DiscoverProfilesResponse:
        """Test DiscoverProfilesResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DiscoverProfilesResponse`
        """
        model = DiscoverProfilesResponse()
        if include_optional:
            return DiscoverProfilesResponse(
                community_profiles = [
                    solomonai_backend_client_sdk.models.community_profile:_the_profile_object_tied_to_a_given_community.CommunityProfile: The profile object tied to a given community(
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
                        algolia_id = 'asndlkhaskhdhasgdahsf-feed-id', )
                    ],
                user_profiles = [
                    solomonai_backend_client_sdk.models.user_profile:_the_profile_object_tied_to_a_given_user.UserProfile: The profile object tied to a given user(
                        id = '', 
                        tags = [
                            solomonai_backend_client_sdk.models.tags:_tags_that_can_be_associated_to_a_record.Tags: tags that can be associated to a record(
                                id = '', 
                                tag_name = 'test-tagname', 
                                description = 'test-description sakjlDKJGSAHGHFDHSGJHFGAHDFJKGSHAJDLgAKSGDHAS CSVDJKSADASKJHDASFDGJKJLHSAHGFJDSAHD kjskhdgfhgdhfgkhsdfdsdfdssdfsdf', )
                            ], 
                        name = 'test-user', 
                        private = True, 
                        followers = '', 
                        following = '', 
                        notification_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                        personal_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                        news_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                        profile_image_url = 'asndlkhaskhdhasgdahsf.jpg', 
                        bookmarks = solomonai_backend_client_sdk.models.bookmark.Bookmark(
                            id = '', 
                            post_ids = [
                                ''
                                ], 
                            publications = [
                                solomonai_backend_client_sdk.models.a_publication_is_a_collections_of_stories_based_around_a_common_theme/_anyone_can_create_them
as_the_creator_of_a_publication,_you're_an_editor_by_default,_which_means_you_have_the_ability_to
a)_add_writers_to_your_publication,
b)_edit_and_publish_the_stories_that_are_submitted_by_your_writers,_and
c)_review_the_metrics_for_all_of_the_stories_that_are_part_of_your_publication/
as_the_publication's_creator,_you'll_also_have_the_ability
to_appoint_new_editors_(so_they_can_do_all_of_that_stuff_i_just_mentioned).A Publication is a collections of stories based around a common theme. Anyone can create them
As the creator of a publication, you're an editor by default, which means you have the ability to
a) add writers to your publication,
b) edit and publish the stories that are submitted by your writers, and
c) review the metrics for all of the stories that are part of your publication.
As the publication's creator, you'll also have the ability
to appoint new editors (so they can do all of that stuff I just mentioned)(
                                    id = '', 
                                    admin = solomonai_backend_client_sdk.models.user_profile:_the_profile_object_tied_to_a_given_user.UserProfile: The profile object tied to a given user(
                                        id = '', 
                                        tags = [
                                            solomonai_backend_client_sdk.models.tags:_tags_that_can_be_associated_to_a_record.Tags: tags that can be associated to a record(
                                                id = '', 
                                                tag_name = 'test-tagname', 
                                                description = 'test-description sakjlDKJGSAHGHFDHSGJHFGAHDFJKGSHAJDLgAKSGDHAS CSVDJKSADASKJHDASFDGJKJLHSAHGFJDSAHD kjskhdgfhgdhfgkhsdfdsdfdssdfsdf', )
                                            ], 
                                        name = 'test-user', 
                                        private = True, 
                                        followers = '', 
                                        following = '', 
                                        notification_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                                        personal_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                                        news_feed_timeline_id = 'asndlkhaskhdhasgdahsf-feed-id', 
                                        profile_image_url = 'asndlkhaskhdhasgdahsf.jpg', 
                                        bookmarks = solomonai_backend_client_sdk.models.bookmark.Bookmark(
                                            id = '', ), 
                                        algolia_id = 'asndlkhaskhdhasgdahsf-feed-id', ), 
                                    admin_backend_platform_user_id = '', 
                                    tags = [
                                        ''
                                        ], 
                                    editors = [
                                        
                                        ], 
                                    subjects = [
                                        ''
                                        ], 
                                    description = '', 
                                    created_at = '', 
                                    type = 'PUBLICATION_TYPE_UNSPECIFIED', 
                                    publication_name = '', )
                                ], ), 
                        algolia_id = 'asndlkhaskhdhasgdahsf-feed-id', )
                    ],
                topics = [
                    solomonai_backend_client_sdk.models.topic:_topic_that_can_be_associated_to_a_record.Topic: topic that can be associated to a record(
                        id = '', 
                        topic_name = 'test-tagname', 
                        description = 'test-description sakjlDKJGSAHGHFDHSGJHFGAHDFJKGSHAJDLgAKSGDHAS CSVDJKSADASKJHDASFDGJKJLHSAHGFJDSAHD kjskhdgfhgdhfgkhsdfdsdfdssdfsdf', 
                        image_url = 'test-tagname', )
                    ]
            )
        else:
            return DiscoverProfilesResponse(
        )
        """

    def testDiscoverProfilesResponse(self):
        """Test DiscoverProfilesResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
