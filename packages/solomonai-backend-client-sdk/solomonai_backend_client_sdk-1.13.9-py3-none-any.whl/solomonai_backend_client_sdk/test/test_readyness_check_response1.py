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

from solomonai_backend_client_sdk.models.readyness_check_response1 import ReadynessCheckResponse1

class TestReadynessCheckResponse1(unittest.TestCase):
    """ReadynessCheckResponse1 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ReadynessCheckResponse1:
        """Test ReadynessCheckResponse1
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ReadynessCheckResponse1`
        """
        model = ReadynessCheckResponse1()
        if include_optional:
            return ReadynessCheckResponse1(
                ready = True
            )
        else:
            return ReadynessCheckResponse1(
        )
        """

    def testReadynessCheckResponse1(self):
        """Test ReadynessCheckResponse1"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
