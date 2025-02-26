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

from solomonai_backend_client_sdk.models.report_comment_response import ReportCommentResponse

class TestReportCommentResponse(unittest.TestCase):
    """ReportCommentResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ReportCommentResponse:
        """Test ReportCommentResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ReportCommentResponse`
        """
        model = ReportCommentResponse()
        if include_optional:
            return ReportCommentResponse(
                comment = solomonai_backend_client_sdk.models.comment.Comment(
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
            )
        else:
            return ReportCommentResponse(
        )
        """

    def testReportCommentResponse(self):
        """Test ReportCommentResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
