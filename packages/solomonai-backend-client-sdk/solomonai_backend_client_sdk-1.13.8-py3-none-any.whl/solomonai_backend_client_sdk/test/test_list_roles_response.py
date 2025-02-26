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

from solomonai_backend_client_sdk.models.list_roles_response import ListRolesResponse

class TestListRolesResponse(unittest.TestCase):
    """ListRolesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ListRolesResponse:
        """Test ListRolesResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListRolesResponse`
        """
        model = ListRolesResponse()
        if include_optional:
            return ListRolesResponse(
                roles = [
                    solomonai_backend_client_sdk.models.role.Role(
                        id = '', 
                        name = '', 
                        type = 'ROLE_TYPE_UNSPECIFIED', 
                        can_create_users = True, 
                        can_read_users = True, 
                        can_update_users = True, 
                        can_delete_users = True, 
                        can_create_projects = True, 
                        can_read_projects = True, 
                        can_update_projects = True, 
                        can_delete_projects = True, 
                        can_create_reports = True, 
                        can_read_reports = True, 
                        can_update_reports = True, 
                        can_delete_reports = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        audit_log = [
                            solomonai_backend_client_sdk.models.role_audit_events.RoleAuditEvents(
                                id = '', 
                                action = 'AUDIT_ACTION_UNSPECIFIED', 
                                performed_by = '', 
                                timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                affected_fields = [
                                    ''
                                    ], 
                                previous_values = [
                                    ''
                                    ], 
                                client_ip = '', 
                                user_agent = '', 
                                context = '', 
                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                            ], 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        assignment_reason = '', 
                        assigned_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        is_active = True, 
                        limitations = [
                            ''
                            ], 
                        role_settings = solomonai_backend_client_sdk.models.additional_role_specific_settings.Additional role-specific settings(), )
                    ],
                total_count = 56
            )
        else:
            return ListRolesResponse(
        )
        """

    def testListRolesResponse(self):
        """Test ListRolesResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
