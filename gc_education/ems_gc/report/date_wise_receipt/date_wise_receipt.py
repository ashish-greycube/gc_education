# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns
from gc_education.ems_gc.report.student_wise_fees_status.student_wise_fees_status import (
    execute as _execute,
)
from frappe.desk.query_report import add_total_row


def execute(filters=None):
    # columns, data = get_columns(), get_data(filters)
    filters["additional_conditions"] = get_additional_conditions(filters)
    columns, data = _execute(filters)
    data = data[:-1]

    fees_data = {d.get("fees"): d for d in data}

    payments = get_data(filters)

    out = []

    for d in payments:
        d.setdefault("paid_amount", 0)
        d.update(fees_data.get(d.fees_name, {}))
        out.append(d)

    columns = [
        col for col in columns if not dict(col).get("fieldname") == "outstanding_amount"
    ] + get_columns()

    add_total_row(out, columns)

    # convert totals row from list to dict
    total_row = out[-1]
    out = out[:-1]
    total_dict = {col["fieldname"]: total_row[idx] for idx, col in enumerate(columns)}
    out.append(total_dict)

    return columns, out


def get_columns():
    return csv_to_columns(
        """
		Posting Date,posting_date,Date,,145
		Receipt No.,payment_entry,Link,Payment Entry,150
		Payment Type,mode_of_payment,,,110
		Cheque No.,reference_no,,,110
		Cheque Dt.,reference_date,Date,,110
		Bank,bank,,,130
    """
    )


def get_data(filters):
    data = frappe.db.sql(
        """
		select 
			tpe.name ,
			tpe.posting_date , coalesce(tpe.paid_amount,0) paid_amount, tpe.company , 
			tpe.branch , tpe.mode_of_payment , tpe.party ,
			tpe.reference_no , tpe.reference_date , tpe.cost_center , tsgs.student ,
			tsgs.group_roll_number , enr.program class, enr.student_batch_name division ,
			enr.academic_year , enr.academic_term , enr.student_name ,
			tpe.bank_name bank ,
            tper.reference_name fees_name
		from `tabPayment Entry` tpe
			inner join `tabProgram Enrollment` enr on enr.docstatus = 1 and enr.student = tpe.party
            inner join `tabProgram` tpr on tpr.name = enr.program
			inner join `tabStudent Group` tsg on tsg.program = enr.program and tsg.academic_term = enr.academic_term 
			inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = enr.student
            left outer join `tabPayment Entry Reference` tper on tper.parent = tpe.name 
                and tper.reference_doctype = 'Fees'
		where tpe.payment_type = 'Receive' and tpe.docstatus = 1 {cond} 
		order by posting_date , class , division 
    """.format(
            cond=get_conditions(filters)
        ),
        filters,
        as_dict=True,
    )

    return data


def get_additional_conditions(filters):
    return """
    and tf.name in (
        select tper.reference_name  from `tabPayment Entry` tpe 
        inner join `tabPayment Entry Reference` tper on tper.parent = tpe.name
        and tper.reference_doctype = 'Fees' 
        and tpe.posting_date >= '{}' and tpe.posting_date <= '{}'
    )
    """.format(
        filters.get("from_date", "2000-01-01"), filters.get("to_date", "2090-01-01")
    )


def get_conditions(filters):
    conditions = []
    if filters.get("academic_year"):
        conditions.append(" enr.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" enr.academic_term = %(academic_term)s")
    if filters.get("batch"):
        lst = filters.batch
        # to prevent SQL Injection
        batches = frappe.get_list("Student Batch Name", pluck="name")
        conditions.append(
            "enr.student_batch_name in ({})".format(
                ",".join(["'%s'" % d for d in lst if d in batches])
            )
        )
    if filters.get("from_date"):
        conditions.append("tpe.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("tpe.posting_date <= %(to_date)s")
    if filters.get("program"):
        lst = filters.program
        # to prevent SQL Injection
        programs = frappe.get_list("Program", pluck="name")
        conditions.append(
            "enr.program in ({})".format(
                ",".join(["'%s'" % d for d in lst if d in programs])
            )
        )
    if filters.get("department"):
        # to prevent SQL Injection
        names = frappe.get_list("Department", pluck="name")
        conditions.append(
            "tpr.department in ({})".format(
                ",".join(["'%s'" % d for d in filters.department if d in names])
            )
        )
    return conditions and " and " + " and ".join(conditions) or ""
