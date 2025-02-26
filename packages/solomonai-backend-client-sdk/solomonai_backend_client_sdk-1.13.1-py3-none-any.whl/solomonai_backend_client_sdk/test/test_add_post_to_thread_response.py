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

from solomonai_backend_client_sdk.models.add_post_to_thread_response import AddPostToThreadResponse

class TestAddPostToThreadResponse(unittest.TestCase):
    """AddPostToThreadResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AddPostToThreadResponse:
        """Test AddPostToThreadResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AddPostToThreadResponse`
        """
        model = AddPostToThreadResponse()
        if include_optional:
            return AddPostToThreadResponse(
                regular_post = solomonai_backend_client_sdk.models.posts:_critical_to_activities_and_define_the_content_sent_over_by_users_and
communities.Posts: Critical to activities and define the content sent over by users and
communities(
                    id = '', 
                    created_at = '', 
                    action = 'POST_TYPE_UNSPECIFIED', 
                    content = '', 
                    mentions = [
                        ''
                        ], 
                    hashtags = [
                        ''
                        ], 
                    media = solomonai_backend_client_sdk.models.media.Media(
                        id = '', 
                        created_at = '', 
                        link = '', 
                        metadata = solomonai_backend_client_sdk.models.media_metadata.MediaMetadata(
                            id = '', 
                            resize = 'MEDIA_RESIZE_UNSPECIFIED', 
                            crop = 'MEDIA_CROP_UNSPECIFIED', 
                            image_width = '', 
                            image_height = '', 
                            type = 'MEDIA_TYPE_UNSPECIFIED', ), ), 
                    extra = {
                        'key' : ''
                        }, 
                    comments = [
                        solomonai_backend_client_sdk.models.comment.Comment(
                            id = '', 
                            backend_platform_user_id = '', 
                            profile_id = '', 
                            mentions = [
                                ''
                                ], 
                            hashtags = [
                                ''
                                ], 
                            created_at = '', 
                            content = '', 
                            replies = [
                                solomonai_backend_client_sdk.models.comment_reply.CommentReply(
                                    id = '', 
                                    backend_platform_user_id = '', 
                                    profile_id = '', 
                                    mentions = [
                                        ''
                                        ], 
                                    hashtags = [
                                        ''
                                        ], 
                                    created_at = '', 
                                    content = '', 
                                    extra = {
                                        'key' : ''
                                        }, 
                                    author_username = 'test-user', 
                                    author_profile_image = 'test-user', 
                                    affinity_score = '', 
                                    quality_score = '', 
                                    user_id_to_affinity_score_map = {
                                        'key' : ''
                                        }, 
                                    author_account_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                                    user_id_to_reaction_map = {
                                        'key' : 'REACTION_UNSPECIFIED'
                                        }, 
                                    user_id_to_reports_map = {
                                        'key' : ''
                                        }, )
                                ], 
                            extra = {
                                'key' : ''
                                }, 
                            author_username = 'test-user', 
                            author_profile_image = 'test-user', 
                            affinity_score = '', 
                            quality_score = '', 
                            user_id_to_affinity_score_map = {
                                'key' : ''
                                }, 
                            user_id_to_reports_map = {
                                'key' : ''
                                }, 
                            author_account_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                            user_id_to_reaction_map = {
                                'key' : 'REACTION_UNSPECIFIED'
                                }, 
                            notes = [
                                solomonai_backend_client_sdk.models.a_note_is_a_response_a_user_can_leave_on_another_user's_piece_of_content/_notes_can
only_be_seen_by_the_user_who_created_the_content_(private)_and_should_serve_as_some_form_of
intimate_feedback_protocol.A note is a response a user can leave on another user's piece of content. Notes can
only be seen by the user who created the content (private) and should serve as some form of
intimate feedback protocol(
                                    id = '', 
                                    backend_platform_user_id = '', 
                                    profile_id = '', 
                                    mentions = [
                                        ''
                                        ], 
                                    hashtags = [
                                        ''
                                        ], 
                                    created_at = '', 
                                    content = '', 
                                    author_user_name = '', 
                                    author_profile_image = '', )
                                ], )
                        ], 
                    backend_platform_user_id = '', 
                    profile_id = '', 
                    title = '', 
                    tags = [
                        ''
                        ], 
                    topic_name = '', 
                    author_username = '', 
                    author_profile_image = '', 
                    affinity_score = '', 
                    quality_score = '', 
                    user_id_to_affinity_score_map = , 
                    insights = solomonai_backend_client_sdk.models.content_insights.ContentInsights(
                        sentence_count = '10', 
                        word_count = '', 
                        language = '', 
                        language_confidence = 1.337, 
                        entities = [
                            solomonai_backend_client_sdk.models.entities.Entities(
                                text = '', 
                                label = '', )
                            ], 
                        sentiment = solomonai_backend_client_sdk.models.sentiment.Sentiment(
                            negative = 30, 
                            neutral = 50, 
                            positive = 89, 
                            compound = 93, ), ), 
                    user_id_to_reports_map = {
                        'key' : ''
                        }, 
                    reading_time = '', 
                    background_image_url = '', 
                    author_account_type = , 
                    notes = [
                        solomonai_backend_client_sdk.models.a_note_is_a_response_a_user_can_leave_on_another_user's_piece_of_content/_notes_can
only_be_seen_by_the_user_who_created_the_content_(private)_and_should_serve_as_some_form_of
intimate_feedback_protocol.A note is a response a user can leave on another user's piece of content. Notes can
only be seen by the user who created the content (private) and should serve as some form of
intimate feedback protocol(
                            id = '', 
                            backend_platform_user_id = '', 
                            profile_id = '', 
                            mentions = [
                                ''
                                ], 
                            hashtags = [
                                ''
                                ], 
                            created_at = '', 
                            content = '', 
                            author_user_name = '', 
                            author_profile_image = '', )
                        ], 
                    thread = solomonai_backend_client_sdk.models.thread.Thread(
                        id = '', 
                        post_ids = [
                            ''
                            ], 
                        parent_post_id = '', 
                        created_at = '', 
                        updated_at = '', ), 
                    thread_participant_type = 'THREAD_PARTICIPANT_TYPE_UNSPECIFIED', 
                    user_id_to_reaction_map = , 
                    ai_generated_question_response = '', 
                    category = 'CATEGORY_UNSPECIFIED', ),
                shared_post = solomonai_backend_client_sdk.models.shared_post:_posts_reshared_by_other_profiles
todo:_need_to_expose_api_endpoints_to_interact_with_shared_posts.SharedPost: Posts reshared by other profiles
TODO: need to expose api endpoints to interact with shared posts(
                    id = '', 
                    original_post_id = 'test-user', 
                    original_author_username = '', 
                    created_at = '', 
                    content = '', 
                    mentions = [
                        ''
                        ], 
                    hashtags = [
                        ''
                        ], 
                    extra = {
                        'key' : ''
                        }, 
                    comments = [
                        solomonai_backend_client_sdk.models.comment.Comment(
                            id = '', 
                            backend_platform_user_id = '', 
                            profile_id = '', 
                            media = solomonai_backend_client_sdk.models.media.Media(
                                id = '', 
                                created_at = '', 
                                link = '', 
                                metadata = solomonai_backend_client_sdk.models.media_metadata.MediaMetadata(
                                    id = '', 
                                    resize = 'MEDIA_RESIZE_UNSPECIFIED', 
                                    crop = 'MEDIA_CROP_UNSPECIFIED', 
                                    image_width = '', 
                                    image_height = '', 
                                    type = 'MEDIA_TYPE_UNSPECIFIED', ), ), 
                            mentions = [
                                ''
                                ], 
                            hashtags = [
                                ''
                                ], 
                            created_at = '', 
                            content = '', 
                            replies = [
                                solomonai_backend_client_sdk.models.comment_reply.CommentReply(
                                    id = '', 
                                    backend_platform_user_id = '', 
                                    profile_id = '', 
                                    mentions = [
                                        ''
                                        ], 
                                    hashtags = [
                                        ''
                                        ], 
                                    created_at = '', 
                                    content = '', 
                                    extra = {
                                        'key' : ''
                                        }, 
                                    author_username = 'test-user', 
                                    author_profile_image = 'test-user', 
                                    affinity_score = '', 
                                    quality_score = '', 
                                    user_id_to_affinity_score_map = {
                                        'key' : ''
                                        }, 
                                    author_account_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                                    user_id_to_reaction_map = {
                                        'key' : 'REACTION_UNSPECIFIED'
                                        }, 
                                    user_id_to_reports_map = {
                                        'key' : ''
                                        }, )
                                ], 
                            extra = {
                                'key' : ''
                                }, 
                            author_username = 'test-user', 
                            author_profile_image = 'test-user', 
                            affinity_score = '', 
                            quality_score = '', 
                            user_id_to_affinity_score_map = {
                                'key' : ''
                                }, 
                            user_id_to_reports_map = {
                                'key' : ''
                                }, 
                            author_account_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                            user_id_to_reaction_map = {
                                'key' : 'REACTION_UNSPECIFIED'
                                }, 
                            notes = [
                                solomonai_backend_client_sdk.models.a_note_is_a_response_a_user_can_leave_on_another_user's_piece_of_content/_notes_can
only_be_seen_by_the_user_who_created_the_content_(private)_and_should_serve_as_some_form_of
intimate_feedback_protocol.A note is a response a user can leave on another user's piece of content. Notes can
only be seen by the user who created the content (private) and should serve as some form of
intimate feedback protocol(
                                    id = '', 
                                    backend_platform_user_id = '', 
                                    profile_id = '', 
                                    mentions = [
                                        ''
                                        ], 
                                    hashtags = [
                                        ''
                                        ], 
                                    created_at = '', 
                                    content = '', 
                                    author_user_name = '', 
                                    author_profile_image = '', )
                                ], )
                        ], 
                    backend_platform_user_id = '', 
                    profile_id = '', 
                    tags = [
                        ''
                        ], 
                    author_username = '', 
                    affinity_score = '', 
                    quality_score = '', 
                    user_id_to_affinity_score_map = , 
                    user_id_to_reports_map = {
                        'key' : ''
                        }, 
                    notes = [
                        solomonai_backend_client_sdk.models.a_note_is_a_response_a_user_can_leave_on_another_user's_piece_of_content/_notes_can
only_be_seen_by_the_user_who_created_the_content_(private)_and_should_serve_as_some_form_of
intimate_feedback_protocol.A note is a response a user can leave on another user's piece of content. Notes can
only be seen by the user who created the content (private) and should serve as some form of
intimate feedback protocol(
                            id = '', 
                            backend_platform_user_id = '', 
                            profile_id = '', 
                            mentions = [
                                ''
                                ], 
                            hashtags = [
                                ''
                                ], 
                            created_at = '', 
                            content = '', 
                            author_user_name = '', 
                            author_profile_image = '', )
                        ], 
                    thread = solomonai_backend_client_sdk.models.thread.Thread(
                        id = '', 
                        post_ids = [
                            ''
                            ], 
                        parent_post_id = '', 
                        created_at = '', 
                        updated_at = '', ), 
                    author_account_type = , 
                    user_id_to_reaction_map = , 
                    action = 'POST_TYPE_UNSPECIFIED', 
                    original_post_user_profile_id = '', 
                    original_post_userbackend_plaform_id = '', 
                    original_post_action = 'POST_TYPE_UNSPECIFIED', 
                    category = 'CATEGORY_UNSPECIFIED', ),
                poll_post = solomonai_backend_client_sdk.models.poll_post.PollPost(
                    id = '', 
                    created_at = '', 
                    action = 'POST_TYPE_UNSPECIFIED', 
                    content = '', 
                    mentions = [
                        ''
                        ], 
                    hashtags = [
                        ''
                        ], 
                    media = solomonai_backend_client_sdk.models.media.Media(
                        id = '', 
                        created_at = '', 
                        link = '', 
                        metadata = solomonai_backend_client_sdk.models.media_metadata.MediaMetadata(
                            id = '', 
                            resize = 'MEDIA_RESIZE_UNSPECIFIED', 
                            crop = 'MEDIA_CROP_UNSPECIFIED', 
                            image_width = '', 
                            image_height = '', 
                            type = 'MEDIA_TYPE_UNSPECIFIED', ), ), 
                    extra = {
                        'key' : ''
                        }, 
                    comments = [
                        solomonai_backend_client_sdk.models.comment.Comment(
                            id = '', 
                            backend_platform_user_id = '', 
                            profile_id = '', 
                            mentions = [
                                ''
                                ], 
                            hashtags = [
                                ''
                                ], 
                            created_at = '', 
                            content = '', 
                            replies = [
                                solomonai_backend_client_sdk.models.comment_reply.CommentReply(
                                    id = '', 
                                    backend_platform_user_id = '', 
                                    profile_id = '', 
                                    mentions = [
                                        ''
                                        ], 
                                    hashtags = [
                                        ''
                                        ], 
                                    created_at = '', 
                                    content = '', 
                                    extra = {
                                        'key' : ''
                                        }, 
                                    author_username = 'test-user', 
                                    author_profile_image = 'test-user', 
                                    affinity_score = '', 
                                    quality_score = '', 
                                    user_id_to_affinity_score_map = {
                                        'key' : ''
                                        }, 
                                    author_account_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                                    user_id_to_reaction_map = {
                                        'key' : 'REACTION_UNSPECIFIED'
                                        }, 
                                    user_id_to_reports_map = {
                                        'key' : ''
                                        }, )
                                ], 
                            extra = {
                                'key' : ''
                                }, 
                            author_username = 'test-user', 
                            author_profile_image = 'test-user', 
                            affinity_score = '', 
                            quality_score = '', 
                            user_id_to_affinity_score_map = {
                                'key' : ''
                                }, 
                            user_id_to_reports_map = {
                                'key' : ''
                                }, 
                            author_account_type = 'ACCOUNT_TYPE_UNSPECIFIED', 
                            user_id_to_reaction_map = {
                                'key' : 'REACTION_UNSPECIFIED'
                                }, 
                            notes = [
                                solomonai_backend_client_sdk.models.a_note_is_a_response_a_user_can_leave_on_another_user's_piece_of_content/_notes_can
only_be_seen_by_the_user_who_created_the_content_(private)_and_should_serve_as_some_form_of
intimate_feedback_protocol.A note is a response a user can leave on another user's piece of content. Notes can
only be seen by the user who created the content (private) and should serve as some form of
intimate feedback protocol(
                                    id = '', 
                                    backend_platform_user_id = '', 
                                    profile_id = '', 
                                    mentions = [
                                        ''
                                        ], 
                                    hashtags = [
                                        ''
                                        ], 
                                    created_at = '', 
                                    content = '', 
                                    author_user_name = '', 
                                    author_profile_image = '', )
                                ], )
                        ], 
                    backend_platform_user_id = '', 
                    profile_id = '', 
                    title = '', 
                    tags = [
                        ''
                        ], 
                    topic_name = '', 
                    author_username = '', 
                    author_profile_image = '', 
                    affinity_score = '', 
                    quality_score = '', 
                    user_id_to_affinity_score_map = , 
                    insights = solomonai_backend_client_sdk.models.content_insights.ContentInsights(
                        sentence_count = '10', 
                        word_count = '', 
                        language = '', 
                        language_confidence = 1.337, 
                        entities = [
                            solomonai_backend_client_sdk.models.entities.Entities(
                                text = '', 
                                label = '', )
                            ], 
                        sentiment = solomonai_backend_client_sdk.models.sentiment.Sentiment(
                            negative = 30, 
                            neutral = 50, 
                            positive = 89, 
                            compound = 93, ), ), 
                    user_id_to_reports_map = {
                        'key' : ''
                        }, 
                    background_image_url = '', 
                    author_account_type = , 
                    user_id_to_poll_responses_map = {
                        'key' : solomonai_backend_client_sdk.models.poll_response.PollResponse(
                            id = '', 
                            user_id = '', 
                            response_value = '', 
                            response_idx = '', )
                        }, 
                    poll_options = [
                        ''
                        ], 
                    poll_distribution = {
                        'key' : 1.337
                        }, 
                    poll_end_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    notes = [
                        solomonai_backend_client_sdk.models.a_note_is_a_response_a_user_can_leave_on_another_user's_piece_of_content/_notes_can
only_be_seen_by_the_user_who_created_the_content_(private)_and_should_serve_as_some_form_of
intimate_feedback_protocol.A note is a response a user can leave on another user's piece of content. Notes can
only be seen by the user who created the content (private) and should serve as some form of
intimate feedback protocol(
                            id = '', 
                            backend_platform_user_id = '', 
                            profile_id = '', 
                            mentions = [
                                ''
                                ], 
                            hashtags = [
                                ''
                                ], 
                            created_at = '', 
                            content = '', 
                            author_user_name = '', 
                            author_profile_image = '', )
                        ], 
                    thread = solomonai_backend_client_sdk.models.thread.Thread(
                        id = '', 
                        post_ids = [
                            ''
                            ], 
                        parent_post_id = '', 
                        created_at = '', 
                        updated_at = '', ), 
                    thread_participant_type = 'THREAD_PARTICIPANT_TYPE_UNSPECIFIED', 
                    user_id_to_reaction_map = , 
                    category = 'CATEGORY_UNSPECIFIED', )
            )
        else:
            return AddPostToThreadResponse(
        )
        """

    def testAddPostToThreadResponse(self):
        """Test AddPostToThreadResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
