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

from solomonai_backend_client_sdk.models.workspaceservicehttp_storage_info import WorkspaceservicehttpStorageInfo

class TestWorkspaceservicehttpStorageInfo(unittest.TestCase):
    """WorkspaceservicehttpStorageInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WorkspaceservicehttpStorageInfo:
        """Test WorkspaceservicehttpStorageInfo
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WorkspaceservicehttpStorageInfo`
        """
        model = WorkspaceservicehttpStorageInfo()
        if include_optional:
            return WorkspaceservicehttpStorageInfo(
                bucket = '',
                key = '',
                location = '',
                type = ''
            )
        else:
            return WorkspaceservicehttpStorageInfo(
        )
        """

    def testWorkspaceservicehttpStorageInfo(self):
        """Test WorkspaceservicehttpStorageInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
