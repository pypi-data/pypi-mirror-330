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

from solomonai_backend_client_sdk.models.ownership_permission import OwnershipPermission

class TestOwnershipPermission(unittest.TestCase):
    """OwnershipPermission unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OwnershipPermission:
        """Test OwnershipPermission
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OwnershipPermission`
        """
        model = OwnershipPermission()
        if include_optional:
            return OwnershipPermission(
                id = '',
                permission_name = '',
                scope = 'PERMISSION_SCOPE_UNSPECIFIED',
                is_delegatable = True,
                requires_approval = True,
                approver_roles = [
                    ''
                    ],
                conditions = solomonai_backend_client_sdk.models.conditions_under_which_this_permission_is_valid.Conditions under which this permission is valid(),
                granted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                permission_audit_logs = [
                    solomonai_backend_client_sdk.models.audit_log.AuditLog(
                        id = '', 
                        actor_type = 'ACTOR_TYPE_UNSPECIFIED', 
                        event_type = 'AUDIT_EVENT_TYPE_UNSPECIFIED', 
                        entity_type = 'ENTITY_TYPE_UNSPECIFIED', 
                        entity_id = '', 
                        change_summary = solomonai_backend_client_sdk.models.change_summary.changeSummary(), 
                        metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                        ip_address = '', 
                        user_agent = '', 
                        geo_location = '', 
                        session_id = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        severity = 'SEVERITY_LEVEL_UNSPECIFIED', 
                        request_id = '', 
                        device_info = '', 
                        platform = '', 
                        user_account_actor_auth0_user_id = '', 
                        business_account_actor_auth0_user_id = '', 
                        team_actor_auth0_user_id = '', 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ]
            )
        else:
            return OwnershipPermission(
        )
        """

    def testOwnershipPermission(self):
        """Test OwnershipPermission"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
