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

from solomonai_backend_client_sdk.models.file_metadata import FileMetadata

class TestFileMetadata(unittest.TestCase):
    """FileMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FileMetadata:
        """Test FileMetadata
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `FileMetadata`
        """
        model = FileMetadata()
        if include_optional:
            return FileMetadata(
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
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return FileMetadata(
        )
        """

    def testFileMetadata(self):
        """Test FileMetadata"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
