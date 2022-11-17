# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report.student_wise_fees_status.student_wise_fees_status import (
    get_data,
)
from gc_education.ems_gc.report import csv_to_columns, _add_total_row
from frappe.desk.query_report import add_total_row


def execute(filters=None):
    columns = get_columns()
    _columns, data = get_data(filters)

    data = [
        d for d in data if isinstance(d, dict) and d.get("outstanding_amount", 0) > 0
    ]

    add_total_row(data, columns)
    return columns, data


def get_columns():
    return csv_to_columns(
        """
        Academic Year,academic_year,,,150
        Academic Term,academic_term,,,150
        Class,program,,,120
        Division,division,,120
        G R No,g_r_number,,,90
        Roll No,group_roll_number,,,90
		ID No.,student,Link,Student,190
        Name,student_name,,,250
		Contact No.,student_mobile_number,,,150
        Quarter,description,,,130
		Pending Amount,outstanding_amount,Currency,,130
		Reference remark,reference_remark,,,300
    """
    )
