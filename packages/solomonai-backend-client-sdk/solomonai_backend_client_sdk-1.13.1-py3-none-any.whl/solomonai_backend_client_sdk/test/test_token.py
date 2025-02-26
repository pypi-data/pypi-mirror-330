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

from solomonai_backend_client_sdk.models.token import Token

class TestToken(unittest.TestCase):
    """Token unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Token:
        """Test Token
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Token`
        """
        model = Token()
        if include_optional:
            return Token(
                id = '',
                item_id = '',
                key_id = '',
                access_token = '',
                version = '',
                merge_end_user_origin_id = '',
                merge_integration_slug = '',
                last_merge_created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return Token(
        )
        """

    def testToken(self):
        """Test Token"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
