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

from solomonai_backend_client_sdk.models.update_bank_account_request import UpdateBankAccountRequest

class TestUpdateBankAccountRequest(unittest.TestCase):
    """UpdateBankAccountRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateBankAccountRequest:
        """Test UpdateBankAccountRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateBankAccountRequest`
        """
        model = UpdateBankAccountRequest()
        if include_optional:
            return UpdateBankAccountRequest(
                bank_account = solomonai_backend_client_sdk.models.bank_account.BankAccount(
                    id = '', 
                    user_id = '', 
                    name = '', 
                    number = '', 
                    type = 'BANK_ACCOUNT_TYPE_UNSPECIFIED', 
                    balance = 1.337, 
                    currency = '', 
                    current_funds = 1.337, 
                    balance_limit = '', 
                    pockets = [
                        solomonai_backend_client_sdk.models.pocket_is_an_abstraction_of_a_over_a_bank_account/_a_user_can_has_at_most_4_pockets_per_connected_account
note:_these_pockets_are_automatically_created_by_the_system_and_should_not_be_exposed_for_mutation
by_any_client/_the_only_operations_that_can_be_performed_against_a_pocket_are:
1/_get_the_pocket
2/_get_the_pocket's_smart_goals
3/_adding_a_smart_goal_to_the_pocket.Pocket is an abstraction of a over a bank account. A user can has at most 4 pockets per connected account
NOTE: these pockets are automatically created by the system and should not be exposed for mutation
by any client. The only operations that can be performed against a pocket are:
1. Get the pocket
2. Get the pocket's smart goals
3. Adding a smart goal to the pocket(
                            id = '', 
                            goals = [
                                solomonai_backend_client_sdk.models.smart_goal.SmartGoal(
                                    id = '', 
                                    user_id = '', 
                                    name = '', 
                                    description = 'Buy a car', 
                                    is_completed = True, 
                                    goal_type = 'GOAL_TYPE_UNSPECIFIED', 
                                    duration = 'Active', 
                                    start_date = 'Active', 
                                    end_date = 'Active', 
                                    target_amount = 'Active', 
                                    current_amount = 'Active', 
                                    milestones = [
                                        solomonai_backend_client_sdk.models.milestone:_represents_a_milestone_in_the_context_of_simfinni/_a_financial_milestone_that_is_both_smart
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
                                        ], 
                                    forecasts = solomonai_backend_client_sdk.models.forecast.Forecast(
                                        id = '', 
                                        forecasted_amount = 'Active', 
                                        forecasted_completion_date = 'Active', 
                                        variance_amount = 'Active', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                                    notes = [
                                        solomonai_backend_client_sdk.models.note_schema.Note schema(
                                            id = '', 
                                            user_id = '', 
                                            content = 'Note content here...', 
                                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                        ], 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            tags = [
                                ''
                                ], 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    plaid_account_id = '', 
                    subtype = '', 
                    status = 'BANK_ACCOUNT_STATUS_UNSPECIFIED', 
                    transactions = [
                        solomonai_backend_client_sdk.models.plaid_account_transaction.PlaidAccountTransaction(
                            account_id = '', 
                            amount = 1.337, 
                            iso_currency_code = '', 
                            unofficial_currency_code = '', 
                            transaction_id = '', 
                            transaction_code = '', 
                            current_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            current_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            authorized_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            authorized_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            category_id = '', 
                            categories = [
                                ''
                                ], 
                            personal_finance_category_primary = '', 
                            personal_finance_category_detailed = '', 
                            transaction_name = '', 
                            merchant_name = '', 
                            check_number = '', 
                            payment_channel = '', 
                            pending = True, 
                            pending_transaction_id = '', 
                            account_owner = '', 
                            payment_meta_by_order_of = '', 
                            payment_meta_payee = '', 
                            payment_meta_payer = '', 
                            payment_meta_payment_method = '', 
                            payment_meta_payment_processor = '', 
                            payment_meta_ppd_id = '', 
                            payment_meta_reason = '', 
                            payment_meta_reference_number = '', 
                            location_address = '', 
                            location_city = '', 
                            location_region = '', 
                            location_postal_code = '', 
                            location_country = '', 
                            location_lat = 1.337, 
                            location_lon = 1.337, 
                            location_store_number = '', 
                            time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            additional_properties = {
                                'key' : null
                                }, 
                            id = '', 
                            user_id = '', 
                            link_id = '', 
                            needs_review = True, 
                            hide_transaction = True, 
                            tags = [
                                ''
                                ], 
                            notes = [
                                solomonai_backend_client_sdk.models.note_schema.Note schema(
                                    id = '', 
                                    user_id = '', 
                                    content = 'Note content here...', 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            splits = [
                                solomonai_backend_client_sdk.models.transaction_split.TransactionSplit(
                                    id = '', 
                                    user_id = '', 
                                    link_id = '', 
                                    description = '', 
                                    amount = 1.337, 
                                    personal_finance_category_primary = '', 
                                    personal_finance_category_detailed = '', 
                                    authorized_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    authorized_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    time_of_split = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    gl_code = '', 
                                    cost_center = '', 
                                    project_code = '', 
                                    tax_amount = 1.337, 
                                    tax_rate = 1.337, 
                                    tax_code = '', 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    created_by_email = '', )
                                ], 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            cost_center = '', 
                            project = '', 
                            tax_amount = 1.337, 
                            tax_rate = 1.337, 
                            tax_code = '', 
                            tax_jurisdiction = '', 
                            tax_type = '', 
                            invoice_number = '', 
                            billing_reference = '', 
                            payment_terms = '', 
                            vendor_id = '', 
                            vendor_name = '', 
                            customer_name = '', 
                            approval_status = 'APPROVAL_STATUS_UNSPECIFIED', 
                            approved_by_email = '', 
                            approved_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            transaction_status = 'TRANSACTION_STATUS_UNSPECIFIED', 
                            attachments = [
                                solomonai_backend_client_sdk.models.attachment.Attachment(
                                    id = '', 
                                    file_name = '', 
                                    file_type = '', 
                                    file_url = '', 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            is_recurring = True, 
                            recurring_frequency = 'RECURRING_FREQUENCY_UNSPECIFIED', 
                            exchange_rate = 1.337, 
                            base_currency_amount = 1.337, 
                            enable_regulatory_compliance = True, 
                            regulatory_compliance_status = 'REGULATORY_COMPLIANCE_STATUS_UNSPECIFIED', 
                            payment_id = '', 
                            settlement_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            risk_score = 1.337, 
                            risk_flags = [
                                ''
                                ], 
                            sox_compliant = True, 
                            gdpr_compliant = True, 
                            assigned_to_user_id = '', )
                        ], 
                    recurring_transactions = [
                        solomonai_backend_client_sdk.models.plaid_account_recurring_transaction.PlaidAccountRecurringTransaction(
                            account_id = '', 
                            stream_id = '', 
                            category_id = '', 
                            description = '', 
                            merchant_name = '', 
                            personal_finance_category_primary = '', 
                            personal_finance_category_detailed = '', 
                            first_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            last_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            frequency = '', 
                            transaction_ids = '', 
                            average_amount = '', 
                            average_amount_iso_currency_code = '', 
                            last_amount = '', 
                            last_amount_iso_currency_code = '', 
                            is_active = True, 
                            updated_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            user_id = '', 
                            link_id = '', 
                            id = '', 
                            flow = '', 
                            time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    statements = [
                        solomonai_backend_client_sdk.models.account_statements_is_a_set_of_statements_tied_to_an_account.AccountStatements is a set of statements tied to an account(
                            id = '', 
                            plaid_statement_id = '', 
                            month = '', 
                            year = '', 
                            statement_pdf_url = '', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    plaid_account_type = '', 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return UpdateBankAccountRequest(
                bank_account = solomonai_backend_client_sdk.models.bank_account.BankAccount(
                    id = '', 
                    user_id = '', 
                    name = '', 
                    number = '', 
                    type = 'BANK_ACCOUNT_TYPE_UNSPECIFIED', 
                    balance = 1.337, 
                    currency = '', 
                    current_funds = 1.337, 
                    balance_limit = '', 
                    pockets = [
                        solomonai_backend_client_sdk.models.pocket_is_an_abstraction_of_a_over_a_bank_account/_a_user_can_has_at_most_4_pockets_per_connected_account
note:_these_pockets_are_automatically_created_by_the_system_and_should_not_be_exposed_for_mutation
by_any_client/_the_only_operations_that_can_be_performed_against_a_pocket_are:
1/_get_the_pocket
2/_get_the_pocket's_smart_goals
3/_adding_a_smart_goal_to_the_pocket.Pocket is an abstraction of a over a bank account. A user can has at most 4 pockets per connected account
NOTE: these pockets are automatically created by the system and should not be exposed for mutation
by any client. The only operations that can be performed against a pocket are:
1. Get the pocket
2. Get the pocket's smart goals
3. Adding a smart goal to the pocket(
                            id = '', 
                            goals = [
                                solomonai_backend_client_sdk.models.smart_goal.SmartGoal(
                                    id = '', 
                                    user_id = '', 
                                    name = '', 
                                    description = 'Buy a car', 
                                    is_completed = True, 
                                    goal_type = 'GOAL_TYPE_UNSPECIFIED', 
                                    duration = 'Active', 
                                    start_date = 'Active', 
                                    end_date = 'Active', 
                                    target_amount = 'Active', 
                                    current_amount = 'Active', 
                                    milestones = [
                                        solomonai_backend_client_sdk.models.milestone:_represents_a_milestone_in_the_context_of_simfinni/_a_financial_milestone_that_is_both_smart
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
                                        ], 
                                    forecasts = solomonai_backend_client_sdk.models.forecast.Forecast(
                                        id = '', 
                                        forecasted_amount = 'Active', 
                                        forecasted_completion_date = 'Active', 
                                        variance_amount = 'Active', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                                    notes = [
                                        solomonai_backend_client_sdk.models.note_schema.Note schema(
                                            id = '', 
                                            user_id = '', 
                                            content = 'Note content here...', 
                                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                        ], 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            tags = [
                                ''
                                ], 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    plaid_account_id = '', 
                    subtype = '', 
                    status = 'BANK_ACCOUNT_STATUS_UNSPECIFIED', 
                    transactions = [
                        solomonai_backend_client_sdk.models.plaid_account_transaction.PlaidAccountTransaction(
                            account_id = '', 
                            amount = 1.337, 
                            iso_currency_code = '', 
                            unofficial_currency_code = '', 
                            transaction_id = '', 
                            transaction_code = '', 
                            current_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            current_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            authorized_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            authorized_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            category_id = '', 
                            categories = [
                                ''
                                ], 
                            personal_finance_category_primary = '', 
                            personal_finance_category_detailed = '', 
                            transaction_name = '', 
                            merchant_name = '', 
                            check_number = '', 
                            payment_channel = '', 
                            pending = True, 
                            pending_transaction_id = '', 
                            account_owner = '', 
                            payment_meta_by_order_of = '', 
                            payment_meta_payee = '', 
                            payment_meta_payer = '', 
                            payment_meta_payment_method = '', 
                            payment_meta_payment_processor = '', 
                            payment_meta_ppd_id = '', 
                            payment_meta_reason = '', 
                            payment_meta_reference_number = '', 
                            location_address = '', 
                            location_city = '', 
                            location_region = '', 
                            location_postal_code = '', 
                            location_country = '', 
                            location_lat = 1.337, 
                            location_lon = 1.337, 
                            location_store_number = '', 
                            time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            additional_properties = {
                                'key' : null
                                }, 
                            id = '', 
                            user_id = '', 
                            link_id = '', 
                            needs_review = True, 
                            hide_transaction = True, 
                            tags = [
                                ''
                                ], 
                            notes = [
                                solomonai_backend_client_sdk.models.note_schema.Note schema(
                                    id = '', 
                                    user_id = '', 
                                    content = 'Note content here...', 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            splits = [
                                solomonai_backend_client_sdk.models.transaction_split.TransactionSplit(
                                    id = '', 
                                    user_id = '', 
                                    link_id = '', 
                                    description = '', 
                                    amount = 1.337, 
                                    personal_finance_category_primary = '', 
                                    personal_finance_category_detailed = '', 
                                    authorized_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    authorized_datetime = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    time_of_split = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    gl_code = '', 
                                    cost_center = '', 
                                    project_code = '', 
                                    tax_amount = 1.337, 
                                    tax_rate = 1.337, 
                                    tax_code = '', 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    created_by_email = '', )
                                ], 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            cost_center = '', 
                            project = '', 
                            tax_amount = 1.337, 
                            tax_rate = 1.337, 
                            tax_code = '', 
                            tax_jurisdiction = '', 
                            tax_type = '', 
                            invoice_number = '', 
                            billing_reference = '', 
                            payment_terms = '', 
                            vendor_id = '', 
                            vendor_name = '', 
                            customer_name = '', 
                            approval_status = 'APPROVAL_STATUS_UNSPECIFIED', 
                            approved_by_email = '', 
                            approved_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            transaction_status = 'TRANSACTION_STATUS_UNSPECIFIED', 
                            attachments = [
                                solomonai_backend_client_sdk.models.attachment.Attachment(
                                    id = '', 
                                    file_name = '', 
                                    file_type = '', 
                                    file_url = '', 
                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                                ], 
                            is_recurring = True, 
                            recurring_frequency = 'RECURRING_FREQUENCY_UNSPECIFIED', 
                            exchange_rate = 1.337, 
                            base_currency_amount = 1.337, 
                            enable_regulatory_compliance = True, 
                            regulatory_compliance_status = 'REGULATORY_COMPLIANCE_STATUS_UNSPECIFIED', 
                            payment_id = '', 
                            settlement_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            risk_score = 1.337, 
                            risk_flags = [
                                ''
                                ], 
                            sox_compliant = True, 
                            gdpr_compliant = True, 
                            assigned_to_user_id = '', )
                        ], 
                    recurring_transactions = [
                        solomonai_backend_client_sdk.models.plaid_account_recurring_transaction.PlaidAccountRecurringTransaction(
                            account_id = '', 
                            stream_id = '', 
                            category_id = '', 
                            description = '', 
                            merchant_name = '', 
                            personal_finance_category_primary = '', 
                            personal_finance_category_detailed = '', 
                            first_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            last_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            frequency = '', 
                            transaction_ids = '', 
                            average_amount = '', 
                            average_amount_iso_currency_code = '', 
                            last_amount = '', 
                            last_amount_iso_currency_code = '', 
                            is_active = True, 
                            updated_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            user_id = '', 
                            link_id = '', 
                            id = '', 
                            flow = '', 
                            time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    statements = [
                        solomonai_backend_client_sdk.models.account_statements_is_a_set_of_statements_tied_to_an_account.AccountStatements is a set of statements tied to an account(
                            id = '', 
                            plaid_statement_id = '', 
                            month = '', 
                            year = '', 
                            statement_pdf_url = '', 
                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], 
                    plaid_account_type = '', 
                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ),
        )
        """

    def testUpdateBankAccountRequest(self):
        """Test UpdateBankAccountRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
