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

from solomonai_backend_client_sdk.models.update_milestone_request import UpdateMilestoneRequest

class TestUpdateMilestoneRequest(unittest.TestCase):
    """UpdateMilestoneRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateMilestoneRequest:
        """Test UpdateMilestoneRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateMilestoneRequest`
        """
        model = UpdateMilestoneRequest()
        if include_optional:
            return UpdateMilestoneRequest(
                milestone = solomonai_backend_client_sdk.models.milestone:_represents_a_milestone_in_the_context_of_simfinni/_a_financial_milestone_that_is_both_smart
and_achievable/_a_milestone_is_a_sub_goal_of_a_goal_and_is_tied_to_a_goal_by_the_goal_id.Milestone: represents a milestone in the context of simfinni. A financial milestone that is both smart
and achievable. A milestone is a sub goal of a goal and is tied to a goal by the goal id(
                    id = '', 
                    name = 'Buy a car', 
                    description = 'Buy a car', 
                    target_date = 'testtagdescription', 
                    target_amount = 'Active', 
                    is_completed = True, 
                    budget = solomonai_backend_client_sdk.models.budget.Budget(
                        id = '', 
                        name = 'Buy a car', 
                        description = '', 
                        start_date = '', 
                        end_date = '', 
                        category = solomonai_backend_client_sdk.models.category1.Category1(
                            id = '', 
                            name = 'Housing', 
                            description = 'Housing is a category primarily for housing', 
                            subcategories = [
                                ''
                                ], 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return UpdateMilestoneRequest(
                milestone = solomonai_backend_client_sdk.models.milestone:_represents_a_milestone_in_the_context_of_simfinni/_a_financial_milestone_that_is_both_smart
and_achievable/_a_milestone_is_a_sub_goal_of_a_goal_and_is_tied_to_a_goal_by_the_goal_id.Milestone: represents a milestone in the context of simfinni. A financial milestone that is both smart
and achievable. A milestone is a sub goal of a goal and is tied to a goal by the goal id(
                    id = '', 
                    name = 'Buy a car', 
                    description = 'Buy a car', 
                    target_date = 'testtagdescription', 
                    target_amount = 'Active', 
                    is_completed = True, 
                    budget = solomonai_backend_client_sdk.models.budget.Budget(
                        id = '', 
                        name = 'Buy a car', 
                        description = '', 
                        start_date = '', 
                        end_date = '', 
                        category = solomonai_backend_client_sdk.models.category1.Category1(
                            id = '', 
                            name = 'Housing', 
                            description = 'Housing is a category primarily for housing', 
                            subcategories = [
                                ''
                                ], 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ),
        )
        """

    def testUpdateMilestoneRequest(self):
        """Test UpdateMilestoneRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
