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

from solomonai_backend_client_sdk.models.remove_tenant_team_member_response import RemoveTenantTeamMemberResponse

class TestRemoveTenantTeamMemberResponse(unittest.TestCase):
    """RemoveTenantTeamMemberResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RemoveTenantTeamMemberResponse:
        """Test RemoveTenantTeamMemberResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RemoveTenantTeamMemberResponse`
        """
        model = RemoveTenantTeamMemberResponse()
        if include_optional:
            return RemoveTenantTeamMemberResponse(
                tenant = solomonai_backend_client_sdk.models.tenant.Tenant(
                    id = '', 
                    display_name = '', 
                    external_id = '', 
                    tenant_type = 'TENANT_TYPE_UNSPECIFIED', 
                    status = 'TENANT_STATUS_UNSPECIFIED', 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    storage_quota = '', 
                    used_storage = '', 
                    metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                    custom_domain = '', 
                    email = '', 
                    is_soft_deleted = True, 
                    is_active = True, 
                    address = solomonai_backend_client_sdk.models.address:_represents_an_account's_address.Address: represents an account's address(
                        id = '', 
                        unit = 'Apt 1', 
                        zipcode = '12345', 
                        city = 'New York', 
                        state = 'NY', 
                        longitude = '-73.987654', 
                        latitude = '40.123456', 
                        addressable_type = 'ADDRESSABLE_TYPE_UNSPECIFIED', 
                        is_primary = True, 
                        address_type = 'ADDRESS_TYPE_UNSPECIFIED', 
                        metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                    phone_number = '', 
                    timezone = '', 
                    language_code = '', 
                    compliance_requirements = [
                        ''
                        ], 
                    feature_flags = solomonai_backend_client_sdk.models.feature_flags.featureFlags(), 
                    security_settings = solomonai_backend_client_sdk.models.security_settings.securitySettings(), 
                    owner_user_id = '', 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    business_accounts = [
                        solomonai_backend_client_sdk.models.business_account.BusinessAccount(
                            id = '', 
                            email = 'example@gmail.com', 
                            username = 'testuser9696', 
                            phone_number = '6513424124', 
                            bio = 'sample description', 
                            headline = 'sample headline', 
                            profile_image_url = '', 
                            company_name = 'Solomon AI', 
                            company_established_date = '', 
                            company_industry_type = 'fintech', 
                            company_website_url = '', 
                            company_description = 'We help businesses succeed', 
                            is_active = True, 
                            is_private = False, 
                            is_email_verified = False, 
                            metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            verified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            last_access = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            authn_account_id = '', 
                            supabase_auth0_user_id = '', 
                            algolia_user_id = '', 
                            base_directory = '', 
                            bucket_location = '', 
                            bucket_name = '', 
                            region = '', 
                            storage_quota = '', 
                            used_storage = '', 
                            tags = [
                                solomonai_backend_client_sdk.models.tags:_represents_metadata_tags_associated_to_an_account.Tags: represents metadata tags associated to an account(
                                    id = '', 
                                    tag_name = 'testtagname', 
                                    tag_description = 'testtagdescription', 
                                    metadata = solomonai_backend_client_sdk.models.metadata_associated_with_tag
validations:
__must_provide_between_1_and_10_metadata_tags.metadata associated with tag
validations:
- must provide between 1 and 10 metadata tags(), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            settings = solomonai_backend_client_sdk.models.settings.Settings(
                                id = '', 
                                app_theme = 'APPLICATION_THEME_UNSPECIFIED', 
                                notification_settings = solomonai_backend_client_sdk.models.notification_settings.NotificationSettings(
                                    id = '', 
                                    notification_type = 'NOTIFICATION_TYPE_UNSPECIFIED', 
                                    alerts = True, ), 
                                preferred_language = '', 
                                risk_tolerance = 'RISK_TOLERANCE_SETTINGS_UNSPECIFIED', 
                                liked_dashboard_panels = [
                                    'LIKED_DASHBOARD_PANELS_UNSPECIFIED'
                                    ], 
                                digital_worker_settings = solomonai_backend_client_sdk.models.digital_worker_settings.DigitalWorkerSettings(
                                    id = '', 
                                    worker_name = '', 
                                    worker_version = '', 
                                    enable_logging = True, ), 
                                financial_preferences = solomonai_backend_client_sdk.models.financial_preferences.FinancialPreferences(
                                    id = '', 
                                    currency_preference = '', 
                                    financial_year_start = '', 
                                    tax_percentage = 1.337, 
                                    tax_code = '', ), ), 
                            account_type = 'PROFILE_TYPE_UNSPECIFIED', 
                            organization = solomonai_backend_client_sdk.models.organization.Organization(
                                id = '', 
                                name = '', 
                                display_name = '', 
                                domain = '', 
                                subscription_tier = 'SUBSCRIPTION_TIER_UNSPECIFIED', 
                                subscription_status = 'SUBSCRIPTION_STATUS_UNSPECIFIED', 
                                email = '', 
                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                is_active = True, 
                                metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                                max_users = '', 
                                technical_contact = '', 
                                owner_supabase_auth_user_id = '', 
                                storage_quota = '', 
                                used_storage = '', 
                                max_workspaces = 56, 
                                max_members = 56, 
                                api_key_prefix = '', 
                                security_settings = solomonai_backend_client_sdk.models.security_settings.securitySettings(), 
                                feature_flags = solomonai_backend_client_sdk.models.feature_flags.featureFlags(), 
                                industry = 'INDUSTRY_TYPE_UNSPECIFIED', 
                                phone_number = '', 
                                website_url = '', 
                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                tenants = [
                                    solomonai_backend_client_sdk.models.tenant.Tenant(
                                        id = '', 
                                        display_name = '', 
                                        external_id = '', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        storage_quota = '', 
                                        used_storage = '', 
                                        metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                                        custom_domain = '', 
                                        email = '', 
                                        is_soft_deleted = True, 
                                        is_active = True, 
                                        phone_number = '', 
                                        timezone = '', 
                                        language_code = '', 
                                        feature_flags = solomonai_backend_client_sdk.models.feature_flags.featureFlags(), 
                                        security_settings = solomonai_backend_client_sdk.models.security_settings.securitySettings(), 
                                        owner_user_id = '', 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        user_accounts = [
                                            solomonai_backend_client_sdk.models.user_account.UserAccount(
                                                id = '', 
                                                email = 'sample@example.com', 
                                                username = 'testuser9696', 
                                                firstname = '', 
                                                lastname = '', 
                                                bio = '', 
                                                headline = '', 
                                                profile_image_url = '', 
                                                phone_number = '', 
                                                is_active = True, 
                                                is_private = True, 
                                                is_email_verified = True, 
                                                metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                                                authn_account_id = '', 
                                                supabase_auth0_user_id = '', 
                                                algolia_user_id = '', 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                verified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                last_access = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                base_directory = '', 
                                                bucket_location = '', 
                                                bucket_name = '', 
                                                region = '', 
                                                storage_quota = '', 
                                                used_storage = '', 
                                                tenant = , 
                                                addresses = [
                                                    solomonai_backend_client_sdk.models.address:_represents_an_account's_address.Address: represents an account's address(
                                                        id = '', 
                                                        unit = 'Apt 1', 
                                                        zipcode = '12345', 
                                                        city = 'New York', 
                                                        state = 'NY', 
                                                        longitude = '-73.987654', 
                                                        latitude = '40.123456', 
                                                        is_primary = True, 
                                                        metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                                    ], 
                                                audit_logs = [
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
                                                    ], 
                                                org_api_keys = [
                                                    solomonai_backend_client_sdk.models.org_api_key.OrgAPIKey(
                                                        id = '', 
                                                        key_name = '', 
                                                        description = '', 
                                                        key_id = '', 
                                                        key_hash = '', 
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
                                                        usage_count = 56, 
                                                        max_usage_count = 56, 
                                                        last_used_ip = '', 
                                                        environment = 'API_KEY_ENVIRONMENT_UNSPECIFIED', 
                                                        revoked = True, 
                                                        revoked_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        revoked_reason = '', 
                                                        expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        created_by = '', 
                                                        last_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        is_active = True, 
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
                                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                                    ], 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        audit_logs = [
                                            solomonai_backend_client_sdk.models.audit_log.AuditLog(
                                                id = '', 
                                                entity_id = '', 
                                                change_summary = solomonai_backend_client_sdk.models.change_summary.changeSummary(), 
                                                metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                                                ip_address = '', 
                                                user_agent = '', 
                                                geo_location = '', 
                                                session_id = '', 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                request_id = '', 
                                                device_info = '', 
                                                platform = '', 
                                                user_account_actor_auth0_user_id = '', 
                                                business_account_actor_auth0_user_id = '', 
                                                team_actor_auth0_user_id = '', 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        tenant_api_keys = [
                                            solomonai_backend_client_sdk.models.tenant_api_key.TenantAPIKey(
                                                id = '', 
                                                key_name = '', 
                                                key_prefix = '', 
                                                key_hash = '', 
                                                key_id = '', 
                                                expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                created_by = '', 
                                                last_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                is_active = True, 
                                                rate_limit = 56, 
                                                permissions = [
                                                    solomonai_backend_client_sdk.models.represents_a_specific_permission_for_a_resource/
@typedef_{object}_permission.Represents a specific permission for a resource.
@typedef {Object} Permission(
                                                        id = '', 
                                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                                    ], 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        tenant_usage_logs = [
                                            solomonai_backend_client_sdk.models.tenant_usage_log.TenantUsageLog(
                                                id = '', 
                                                timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                quantity = '', 
                                                unit = 'STORAGE_UNIT_UNSPECIFIED', 
                                                details = '', 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        record_id_reference = '', )
                                    ], 
                                org_members = [
                                    solomonai_backend_client_sdk.models.org_member.OrgMember(
                                        id = '', 
                                        role = solomonai_backend_client_sdk.models.role.Role(
                                            id = '', 
                                            name = '', 
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
                                            role_settings = solomonai_backend_client_sdk.models.additional_role_specific_settings.Additional role-specific settings(), ), 
                                        email = '', 
                                        name = '', 
                                        joined_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        invited_by_email = '', 
                                        last_access = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        permissions = [
                                            'PERMISSION_TYPE_UNSPECIFIED'
                                            ], 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                org_api_keys = [
                                    solomonai_backend_client_sdk.models.org_api_key.OrgAPIKey(
                                        id = '', 
                                        key_name = '', 
                                        description = '', 
                                        key_id = '', 
                                        key_hash = '', 
                                        rate_limit = 56, 
                                        usage_count = 56, 
                                        max_usage_count = 56, 
                                        last_used_ip = '', 
                                        revoked = True, 
                                        revoked_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        revoked_reason = '', 
                                        expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        created_by = '', 
                                        last_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        is_active = True, 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                org_usage_logs = [
                                    solomonai_backend_client_sdk.models.org_usage_log.OrgUsageLog(
                                        id = '', 
                                        timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        quantity = '', 
                                        details = '', 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                audit_logs = [
                                    
                                    ], 
                                record_id_reference = '', 
                                regulatory_status = 'REGULATORY_STATUS_UNSPECIFIED', 
                                license_numbers = [
                                    ''
                                    ], 
                                compliance_tier = 'COMPLIANCE_TIER_UNSPECIFIED', 
                                kyc_provider = '', 
                                payment_provider = '', 
                                transaction_limit = '', 
                                risk_score = 1.337, ), 
                            tenant = , 
                            addresses = [
                                
                                ], 
                            audit_logs = [
                                
                                ], 
                            org_api_keys = [
                                
                                ], 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    user_accounts = [
                        solomonai_backend_client_sdk.models.user_account.UserAccount(
                            id = '', 
                            email = 'sample@example.com', 
                            username = 'testuser9696', 
                            firstname = '', 
                            lastname = '', 
                            bio = '', 
                            headline = '', 
                            profile_image_url = '', 
                            phone_number = '', 
                            is_active = True, 
                            is_private = True, 
                            is_email_verified = True, 
                            metadata = solomonai_backend_client_sdk.models.metadata.metadata(), 
                            authn_account_id = '', 
                            supabase_auth0_user_id = '', 
                            algolia_user_id = '', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            verified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            last_access = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            base_directory = '', 
                            bucket_location = '', 
                            bucket_name = '', 
                            region = '', 
                            storage_quota = '', 
                            used_storage = '', 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    settings = solomonai_backend_client_sdk.models.settings.Settings(
                        id = '', 
                        preferred_language = '', ), 
                    audit_logs = , 
                    tenant_api_keys = [
                        solomonai_backend_client_sdk.models.tenant_api_key.TenantAPIKey(
                            id = '', 
                            key_name = '', 
                            key_prefix = '', 
                            key_hash = '', 
                            key_id = '', 
                            expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            created_by = '', 
                            last_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            is_active = True, 
                            rate_limit = 56, 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    tenant_usage_logs = [
                        solomonai_backend_client_sdk.models.tenant_usage_log.TenantUsageLog(
                            id = '', 
                            timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            quantity = '', 
                            details = '', 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    record_id_reference = '', )
            )
        else:
            return RemoveTenantTeamMemberResponse(
        )
        """

    def testRemoveTenantTeamMemberResponse(self):
        """Test RemoveTenantTeamMemberResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
