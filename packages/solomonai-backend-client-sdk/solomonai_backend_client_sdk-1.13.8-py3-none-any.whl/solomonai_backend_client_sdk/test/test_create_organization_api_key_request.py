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

from solomonai_backend_client_sdk.models.create_organization_api_key_request import CreateOrganizationApiKeyRequest

class TestCreateOrganizationApiKeyRequest(unittest.TestCase):
    """CreateOrganizationApiKeyRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateOrganizationApiKeyRequest:
        """Test CreateOrganizationApiKeyRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateOrganizationApiKeyRequest`
        """
        model = CreateOrganizationApiKeyRequest()
        if include_optional:
            return CreateOrganizationApiKeyRequest(
                organization_id = '',
                owner_supabase_auth_user_id = '',
                key_name = '',
                scopes = [
                    'SCOPE_TYPE_UNSPECIFIED'
                    ],
                rate_limit = 56,
                allowed_ips = [
                    ''
                    ],
                allowed_domains = [
                    ''
                    ],
                max_usage_count = 56,
                environment = 'API_KEY_ENVIRONMENT_UNSPECIFIED',
                expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return CreateOrganizationApiKeyRequest(
                organization_id = '',
                owner_supabase_auth_user_id = '',
                key_name = '',
        )
        """

    def testCreateOrganizationApiKeyRequest(self):
        """Test CreateOrganizationApiKeyRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
