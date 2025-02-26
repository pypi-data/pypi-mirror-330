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

from solomonai_backend_client_sdk.models.get_single_comment_thread_response import GetSingleCommentThreadResponse

class TestGetSingleCommentThreadResponse(unittest.TestCase):
    """GetSingleCommentThreadResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetSingleCommentThreadResponse:
        """Test GetSingleCommentThreadResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetSingleCommentThreadResponse`
        """
        model = GetSingleCommentThreadResponse()
        if include_optional:
            return GetSingleCommentThreadResponse(
                thread = solomonai_backend_client_sdk.models.comment_thread.CommentThread(
                    id = '', 
                    file_id = '', 
                    root_comment = solomonai_backend_client_sdk.models.comment1.Comment1(
                        id = '', 
                        thread_id = '', 
                        tenant_id = '', 
                        author_name = '', 
                        content = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        parent_comment_id = '', 
                        status = '', 
                        reactions = {
                            'key' : 56
                            }, 
                        edits = [
                            solomonai_backend_client_sdk.models.comment_edit.CommentEdit(
                                id = '', 
                                edited_content = '', 
                                edited_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                            ], 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        tags = [
                            ''
                            ], ), 
                    replies = [
                        solomonai_backend_client_sdk.models.comment1.Comment1(
                            id = '', 
                            thread_id = '', 
                            tenant_id = '', 
                            author_name = '', 
                            content = '', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            parent_comment_id = '', 
                            status = '', 
                            reactions = {
                                'key' : 56
                                }, 
                            edits = [
                                solomonai_backend_client_sdk.models.comment_edit.CommentEdit(
                                    id = '', 
                                    edited_content = '', 
                                    edited_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    status = '', 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    from = 56, 
                    to = 56, 
                    version_id = '', 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return GetSingleCommentThreadResponse(
        )
        """

    def testGetSingleCommentThreadResponse(self):
        """Test GetSingleCommentThreadResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
