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
        Class,class,,,120
        Division,division,,120
        Roll No.,group_roll_number,,Int,120
		ID No.,party,Link,Student,190
        Name,student_name,,,250
		Posting Date,posting_date,Date,,145
		Receipt No.,name,Link,Payment Entry,150
		Payment Type,mode_of_payment,,,110
		Cheque No.,reference_no,,,110
		Cheque Dt.,reference_date,Date,,110
		Bank,bank,,,130
		Amount,paid_amount,Currency,,110
    """
    )


def get_data(filters):
    data = frappe.db.sql(
        """
		select 
			tpe.name ,
			tpe.posting_date , tpe.paid_amount , tpe.company , 
			tpe.branch , tpe.mode_of_payment , tpe.party ,
			tpe.reference_no , tpe.reference_date , tpe.cost_center , 
			tsgs.group_roll_number , enr.program class, enr.student_batch_name division ,
			enr.academic_year , enr.academic_term , enr.student_name ,
			tpe.bank_name bank
		from `tabPayment Entry` tpe
			inner join `tabProgram Enrollment` enr on enr.student = tpe.party
			inner join `tabStudent Group` tsg on tsg.program = enr.program and tsg.academic_term = enr.academic_term 
			inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = enr.student
		where tpe.payment_type = 'Receive' and tpe.docstatus = 1 {cond} 
		order by posting_date , class , division 
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
        conditions.append(" enr.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" enr.academic_term = %(academic_term)s")
    if filters.get("program"):
        conditions.append(" enr.program = %(program)s")
    if filters.get("batch"):
        conditions.append(" enr.student_batch_name = %(batch)s")
    if filters.get("from_date"):
        conditions.append("tpe.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("tpe.posting_date <= %(to_date)s")

    return conditions and " and " + " and ".join(conditions) or ""
