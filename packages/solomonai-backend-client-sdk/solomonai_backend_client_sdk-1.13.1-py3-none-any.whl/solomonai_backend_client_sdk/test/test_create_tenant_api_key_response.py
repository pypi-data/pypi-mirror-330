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

from solomonai_backend_client_sdk.models.create_tenant_api_key_response import CreateTenantApiKeyResponse

class TestCreateTenantApiKeyResponse(unittest.TestCase):
    """CreateTenantApiKeyResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateTenantApiKeyResponse:
        """Test CreateTenantApiKeyResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateTenantApiKeyResponse`
        """
        model = CreateTenantApiKeyResponse()
        if include_optional:
            return CreateTenantApiKeyResponse(
                api_key = solomonai_backend_client_sdk.models.tenant_api_key.TenantAPIKey(
                    id = '', 
                    key_name = '', 
                    key_prefix = '', 
                    key_hash = '', 
                    key_id = '', 
                    scopes = [
                        'SCOPE_TYPE_UNSPECIFIED'
                        ], 
                    expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    created_by = '', 
                    last_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    is_active = True, 
                    environment = 'API_KEY_ENVIRONMENT_UNSPECIFIED', 
                    rate_limit = 56, 
                    allowed_ips = [
                        ''
                        ], 
                    allowed_domains = [
                        ''
                        ], 
                    permissions = [
                        solomonai_backend_client_sdk.models.represents_a_specific_permission_for_a_resource/
@typedef_{object}_permission.Represents a specific permission for a resource.
@typedef {Object} Permission(
                            id = '', 
                            type = 'PERMISSION_TYPE_UNSPECIFIED', 
                            resource = 'RESOURCE_TYPE_UNSPECIFIED', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ),
                key_id = ''
            )
        else:
            return CreateTenantApiKeyResponse(
        )
        """

    def testCreateTenantApiKeyResponse(self):
        """Test CreateTenantApiKeyResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
