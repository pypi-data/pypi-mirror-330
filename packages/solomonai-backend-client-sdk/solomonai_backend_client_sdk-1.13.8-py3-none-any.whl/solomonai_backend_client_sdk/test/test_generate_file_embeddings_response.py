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

from solomonai_backend_client_sdk.models.generate_file_embeddings_response import GenerateFileEmbeddingsResponse

class TestGenerateFileEmbeddingsResponse(unittest.TestCase):
    """GenerateFileEmbeddingsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GenerateFileEmbeddingsResponse:
        """Test GenerateFileEmbeddingsResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GenerateFileEmbeddingsResponse`
        """
        model = GenerateFileEmbeddingsResponse()
        if include_optional:
            return GenerateFileEmbeddingsResponse(
                status = 'BACKGROUND_JOB_STATUS_UNSPECIFIED',
                job_id = '',
                estimated_completion_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return GenerateFileEmbeddingsResponse(
        )
        """

    def testGenerateFileEmbeddingsResponse(self):
        """Test GenerateFileEmbeddingsResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
