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

from solomonai_backend_client_sdk.models.create_comment_edit_response import CreateCommentEditResponse

class TestCreateCommentEditResponse(unittest.TestCase):
    """CreateCommentEditResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateCommentEditResponse:
        """Test CreateCommentEditResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateCommentEditResponse`
        """
        model = CreateCommentEditResponse()
        if include_optional:
            return CreateCommentEditResponse(
                edit = solomonai_backend_client_sdk.models.comment_edit.CommentEdit(
                    id = '', 
                    edited_content = '', 
                    edited_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return CreateCommentEditResponse(
        )
        """

    def testCreateCommentEditResponse(self):
        """Test CreateCommentEditResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
