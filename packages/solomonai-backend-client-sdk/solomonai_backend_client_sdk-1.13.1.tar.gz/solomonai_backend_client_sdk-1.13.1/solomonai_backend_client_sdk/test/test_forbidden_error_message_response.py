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

from solomonai_backend_client_sdk.models.forbidden_error_message_response import ForbiddenErrorMessageResponse

class TestForbiddenErrorMessageResponse(unittest.TestCase):
    """ForbiddenErrorMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ForbiddenErrorMessageResponse:
        """Test ForbiddenErrorMessageResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ForbiddenErrorMessageResponse`
        """
        model = ForbiddenErrorMessageResponse()
        if include_optional:
            return ForbiddenErrorMessageResponse(
                code = 56,
                message = '',
                reason = '',
                required_permissions = [
                    ''
                    ],
                error_response = solomonai_backend_client_sdk.models.base_error_message_response,_extending_google/rpc/status.Base error message response, extending google.rpc.Status(
                    status = solomonai_backend_client_sdk.models.status.Status(
                        code = 56, 
                        message = '', 
                        details = [
                            {
                                'key' : null
                                }
                            ], ), )
            )
        else:
            return ForbiddenErrorMessageResponse(
        )
        """

    def testForbiddenErrorMessageResponse(self):
        """Test ForbiddenErrorMessageResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
