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

from solomonai_backend_client_sdk.models.workspace import Workspace

class TestWorkspace(unittest.TestCase):
    """Workspace unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Workspace:
        """Test Workspace
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Workspace`
        """
        model = Workspace()
        if include_optional:
            return Workspace(
                id = '',
                name = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                tags = [
                    ''
                    ],
                folders = [
                    solomonai_backend_client_sdk.models.folder_metadata.FolderMetadata(
                        id = '', 
                        name = '', 
                        child_folder = [
                            solomonai_backend_client_sdk.models.folder_metadata.FolderMetadata(
                                id = '', 
                                name = '', 
                                child_folder = [
                                    
                                    ], 
                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                files = [
                                    solomonai_backend_client_sdk.models.file_metadata.FileMetadata(
                                        id = '', 
                                        name = '', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        size = '', 
                                        file_type = '', 
                                        tags = [
                                            ''
                                            ], 
                                        is_deleted = True, 
                                        version = 56, 
                                        s3_key = '', 
                                        s3_bucket_name = '', 
                                        s3_region = '', 
                                        s3_version_id = '', 
                                        s3_etag = '', 
                                        s3_content_type = '', 
                                        s3_content_length = '', 
                                        s3_content_encoding = '', 
                                        s3_content_disposition = '', 
                                        s3_last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        s3_storage_class = '', 
                                        s3_server_side_encryption = '', 
                                        s3_acl = '', 
                                        s3_metadata = {
                                            'key' : ''
                                            }, 
                                        version_id = '', 
                                        upload_id = '', 
                                        location = '', 
                                        markdown_content = '', 
                                        mime_type = '', 
                                        checksum = '', 
                                        preview_available = True, 
                                        preview_status = '', 
                                        thumbnail_url = '', 
                                        last_accessed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        access_count = 56, 
                                        embeddings = solomonai_backend_client_sdk.models.file_embeddings.FileEmbeddings(
                                            id = '', 
                                            file_id = '', 
                                            chunk_index = 56, 
                                            chunk_text = '', 
                                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                                        versions = [
                                            solomonai_backend_client_sdk.models.file_versions.FileVersions(
                                                id = '', 
                                                file_id = '', 
                                                version_number = 56, 
                                                s3_version_id = '', 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                size = '', 
                                                checksum = '', 
                                                modified_by = '', 
                                                change_summary = '', 
                                                snapshot = solomonai_backend_client_sdk.models.document_snapshot.DocumentSnapshot(
                                                    id = '', 
                                                    file_id = '', 
                                                    version_id = '', 
                                                    content = '', 
                                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    snapshot_type = '', 
                                                    created_by_tenant_id = '', 
                                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        comment_threads = [
                                            solomonai_backend_client_sdk.models.comment_thread.CommentThread(
                                                id = '', 
                                                file_id = '', 
                                                root_comment = solomonai_backend_client_sdk.models.comment1.Comment1(
                                                    id = '', 
                                                    thread_id = '', 
                                                    tenant_id = '', 
                                                    author_name = '', 
                                                    content = '', 
                                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    parent_comment_id = '', 
                                                    status = '', 
                                                    reactions = {
                                                        'key' : 56
                                                        }, 
                                                    edits = [
                                                        solomonai_backend_client_sdk.models.comment_edit.CommentEdit(
                                                            id = '', 
                                                            edited_content = '', 
                                                            edited_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                                        ], 
                                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    tags = [
                                                        ''
                                                        ], ), 
                                                replies = [
                                                    solomonai_backend_client_sdk.models.comment1.Comment1(
                                                        id = '', 
                                                        thread_id = '', 
                                                        tenant_id = '', 
                                                        author_name = '', 
                                                        content = '', 
                                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        parent_comment_id = '', 
                                                        status = '', 
                                                        reactions = {
                                                            'key' : 56
                                                            }, 
                                                        edits = [
                                                            solomonai_backend_client_sdk.models.comment_edit.CommentEdit(
                                                                id = '', 
                                                                edited_content = '', 
                                                                edited_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                                            ], 
                                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                                    ], 
                                                status = '', 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                from = 56, 
                                                to = 56, 
                                                version_id = '', 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        shared_links = [
                                            solomonai_backend_client_sdk.models.file_sharing.FileSharing(
                                                id = '', 
                                                file_id = '', 
                                                shared_link = '', 
                                                permission_level = 'SHARE_PERMISSION_UNSPECIFIED', 
                                                expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                last_accessed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                is_active = True, 
                                                password = '', 
                                                max_accesses = 56, 
                                                access_count = 56, 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        snapshots = [
                                            solomonai_backend_client_sdk.models.document_snapshot.DocumentSnapshot(
                                                id = '', 
                                                file_id = '', 
                                                version_id = '', 
                                                content = '', 
                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                snapshot_type = '', 
                                                created_by_tenant_id = '', 
                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                            ], 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                is_deleted = True, 
                                s3_bucket_name = '', 
                                s3_folder_path = '', 
                                s3_region = '', 
                                s3_metadata = {
                                    'key' : ''
                                    }, 
                                s3_acl = '', 
                                s3_last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                version_id = '', 
                                description = '', 
                                metadata_json = '', 
                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                            ], 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        files = [
                            solomonai_backend_client_sdk.models.file_metadata.FileMetadata(
                                id = '', 
                                name = '', 
                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                size = '', 
                                file_type = '', 
                                is_deleted = True, 
                                version = 56, 
                                s3_key = '', 
                                s3_bucket_name = '', 
                                s3_region = '', 
                                s3_version_id = '', 
                                s3_etag = '', 
                                s3_content_type = '', 
                                s3_content_length = '', 
                                s3_content_encoding = '', 
                                s3_content_disposition = '', 
                                s3_last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                s3_storage_class = '', 
                                s3_server_side_encryption = '', 
                                s3_acl = '', 
                                version_id = '', 
                                upload_id = '', 
                                location = '', 
                                markdown_content = '', 
                                mime_type = '', 
                                checksum = '', 
                                preview_available = True, 
                                preview_status = '', 
                                thumbnail_url = '', 
                                last_accessed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                access_count = 56, 
                                versions = [
                                    solomonai_backend_client_sdk.models.file_versions.FileVersions(
                                        id = '', 
                                        file_id = '', 
                                        version_number = 56, 
                                        s3_version_id = '', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        size = '', 
                                        checksum = '', 
                                        modified_by = '', 
                                        change_summary = '', 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                comment_threads = [
                                    solomonai_backend_client_sdk.models.comment_thread.CommentThread(
                                        id = '', 
                                        file_id = '', 
                                        replies = [
                                            
                                            ], 
                                        status = '', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        from = 56, 
                                        to = 56, 
                                        version_id = '', 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                shared_links = [
                                    solomonai_backend_client_sdk.models.file_sharing.FileSharing(
                                        id = '', 
                                        file_id = '', 
                                        shared_link = '', 
                                        expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        last_accessed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        is_active = True, 
                                        password = '', 
                                        max_accesses = 56, 
                                        access_count = 56, 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                    ], 
                                snapshots = [
                                    
                                    ], 
                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                            ], 
                        is_deleted = True, 
                        s3_bucket_name = '', 
                        s3_folder_path = '', 
                        s3_region = '', 
                        s3_metadata = {
                            'key' : ''
                            }, 
                        s3_acl = '', 
                        s3_last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        version_id = '', 
                        description = '', 
                        metadata_json = '', 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                version = 56,
                is_deleted = True,
                s3_bucket_name = '',
                s3_folder_path = '',
                s3_region = '',
                s3_metadata = {
                    'key' : ''
                    },
                s3_acl = '',
                s3_last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                unique_identifier = '',
                version_id = '',
                description = '',
                metadata_json = '',
                storage_quota = '',
                used_storage = '',
                tenant_id = '',
                organization_id = '',
                workspace_type = '',
                parent_workspace_id = '',
                workspace_path = '',
                icon_url = '',
                color_theme = '',
                is_template = True,
                template_id = '',
                favorite_count = 56,
                last_activity = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                retention_days = 56,
                default_view = '',
                max_file_size = '',
                max_storage_per_user = '',
                max_versions = 56,
                allow_public_sharing = True,
                require_approval = True,
                member_limit = 56,
                guest_access = True,
                sharing = [
                    solomonai_backend_client_sdk.models.workspace_sharing.WorkspaceSharing(
                        id = '', 
                        shared_with_user_id = '', 
                        sharing_type = '', 
                        permission_level = 'SHARE_PERMISSION_UNSPECIFIED', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        created_by_user_id = '', 
                        access_key = '', 
                        is_active = True, 
                        last_accessed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                activity = [
                    solomonai_backend_client_sdk.models.workspace_activity.WorkspaceActivity(
                        id = '', 
                        tenant_id = '', 
                        action_type = '', 
                        action_details_json = '', 
                        timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        ip_address = '', 
                        user_agent = '', 
                        affected_items = [
                            ''
                            ], 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                compliance = [
                    solomonai_backend_client_sdk.models.workspace_compliance.WorkspaceCompliance(
                        id = '', 
                        tenant_id = '', 
                        retention_policy_json = solomonai_backend_client_sdk.models.json_as_string.JSON as string(), 
                        encryption_settings_json = solomonai_backend_client_sdk.models.json_as_string.JSON as string(), 
                        compliance_level = '', 
                        audit_frequency = '', 
                        last_audit = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        required_tags = [
                            ''
                            ], 
                        restricted_actions = [
                            ''
                            ], 
                        gdpr_compliant = True, 
                        hipaa_compliant = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return Workspace(
        )
        """

    def testWorkspace(self):
        """Test Workspace"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
