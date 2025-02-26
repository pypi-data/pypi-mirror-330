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

from solomonai_backend_client_sdk.models.employee_payroll_run import EmployeePayrollRun

class TestEmployeePayrollRun(unittest.TestCase):
    """EmployeePayrollRun unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> EmployeePayrollRun:
        """Test EmployeePayrollRun
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EmployeePayrollRun`
        """
        model = EmployeePayrollRun()
        if include_optional:
            return EmployeePayrollRun(
                id = '',
                remote_id = '',
                gross_pay = 1.337,
                net_pay = 1.337,
                start_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                end_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                check_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                earnings = [
                    solomonai_backend_client_sdk.models.earning.Earning(
                        id = '', 
                        remote_id = '', 
                        amount = 1.337, 
                        type = 'EARNING_TYPE_UNSPECIFIED', 
                        remote_was_deleted = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        payroll_run_merge_account_id = '', 
                        merge_account_id = '', 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                deductions = [
                    solomonai_backend_client_sdk.models.deduction.Deduction(
                        id = '', 
                        remote_id = '', 
                        name = '', 
                        employee_deduction = 1.337, 
                        company_deduction = 1.337, 
                        remote_was_deleted = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        payroll_run_merge_account_id = '', 
                        merge_account_id = '', 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                taxes = [
                    solomonai_backend_client_sdk.models.tax.Tax(
                        id = '', 
                        remote_id = '', 
                        name = '', 
                        amount = 1.337, 
                        employer_tax = True, 
                        remote_was_deleted = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        payroll_run_merge_account_id = '', 
                        merge_account_id = '', 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                remote_was_deleted = True,
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                modified_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                payroll_run_merge_account_id = '',
                employee_merge_account_id = '',
                merge_account_id = '',
                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return EmployeePayrollRun(
        )
        """

    def testEmployeePayrollRun(self):
        """Test EmployeePayrollRun"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
