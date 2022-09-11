# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return csv_to_columns(
        """
        Academic Year,academic_year,,,150
        Academic Term,academic_term,,,150
        Class,program,,,120
        Division,division,,120
		ID No.,student,Link,Student,190
        Name,student_name,,,250
		Total Amount,grand_total,Currency,,130
		Additional Amount,additional_amount,Currency,,130
		Exemption Amount,exemption_amount,Currency,,130
		NA Amount,na_amount,Currency,,130
		Paid Amount,paid_amount,Currency,,130
		Pending Amount,outstanding_amount,Currency,,130
    """
    )


def get_data(filters):
    data = frappe.db.sql(
        """
	select 
		tfs.academic_year , tfs.academic_term , tfs.program ,
		tf.student , tf.student_name , tf.grand_total , tf.outstanding_amount , 
		tf.grand_total - tf.outstanding_amount paid_amount , 
		tf.branch , tf.cost_center , tsg.batch division , 
        ts.student_mobile_number , tsgs.group_roll_number
	from `tabFee Schedule` tfs 
	inner join `tabFee Schedule Student Group` tfssg on tfssg.parent = tfs.name
	inner join `tabStudent Group` tsg on tsg.name = tfssg.student_group 
	inner JOIN tabFees tf on tf.fee_schedule = tfs.name
    inner join tabStudent ts on ts.name = tf.student
    inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = ts.name 
    {cond}
    order by tfs.program , tsg.batch , tsgs.group_roll_number
    """.format(
            cond=get_conditions(filters)
        ),
        filters,
        as_dict=True,
    )

    return data


def get_conditions(filters):
    conditions = []
    if filters.get("academic_year"):
        conditions.append(" tfs.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" tfs.academic_term = %(academic_term)s")
    if filters.get("program"):
        conditions.append(" tfs.program = %(program)s")
    if filters.get("batch"):
        conditions.append(" tsg.batch = %(batch)s")
    return conditions and "where" + " and ".join(conditions) or ""
