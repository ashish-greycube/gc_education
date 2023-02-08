# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns
from frappe.utils import cstr


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_data(filters):

    data = frappe.db.sql(
        """
    select 
        tpe.academic_year , tpe.academic_term , 
        tpe.program , tpe.student_batch_name , 
        ts.g_r_number , tsgs.group_roll_number , ts.title ,
        case tsgs.active when 1 then 'Active' else 'Inactive' end class_status ,
        case 
            when ts.enabled = 1 then 'Enabled' 
            when ts.date_of_leaving is not null and ts.date_of_leaving > %(as_on_date)s then 'Enabled'
            else 'Disabled' end student_status ,
        ts.leaving_certificate_number , tsg.name student_group , tpe.name program_enrollment ,
        if(tpr.sort_order_cf=0,10000,tpr.sort_order_cf) sort_order
    from tabStudent ts 
    inner join `tabProgram Enrollment` tpe on tpe.docstatus = 1 and tpe.student = ts.name 
    inner join `tabProgram` tpr on tpr.name = tpe.program
    inner join `tabStudent Group` tsg on tsg.program = tpe.program and tsg.academic_term = tpe.academic_term 
    inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = ts.name 
    {cond}
    order by sort_order , tpe.student_batch_name , tsgs.group_roll_number , ts.g_r_number 
    """.format(
            cond=get_conditions(filters)
        ),
        filters,
        as_dict=True,
    )
    data.append(
        {
            "bold": 1,
            "class_status": frappe.bold("Total"),
            "title": frappe.bold(cstr(len(data))),
        }
    )

    return data


def get_conditions(filters):
    conditions = []
    if filters.get("student"):
        conditions.append(" ts.name = %(student)s")

    if filters.get("academic_year"):
        conditions.append(" tpe.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" tpe.academic_term = %(academic_term)s")
    if filters.get("batch"):
        lst = filters.batch
        # to prevent SQL Injection
        batches = frappe.get_list("Student Batch Name", pluck="name")
        conditions.append(
            "tpe.student_batch_name in ({})".format(
                ",".join(["'%s'" % d for d in lst if d in batches])
            )
        )
    if filters.get("student_status") and not filters.student_status == "All":
        conditions.append(
            "ts.enabled = {}".format(
                filters.get("student_status") == "Enabled" and 1 or 0
            )
        )
    if filters.get("program"):
        lst = filters.program
        # to prevent SQL Injection
        programs = frappe.get_list("Program", pluck="name")
        conditions.append(
            "tpe.program in ({})".format(
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
    return conditions and " where " + " and ".join(conditions) or ""


def get_columns():
    return csv_to_columns(
        """
        Academic Year,academic_year,,,150
        Academic Term,academic_term,,,150
        Class,program,,,190
        Division,student_batch_name,,,190
        GR No.,g_r_number,,,120
        Roll No.,group_roll_number,,Int,120
        Name,title,,,290
        Student Status,student_status,,,120
        Class Status,class_status,,,120
        LC Number,leaving_certificate_number,,,130
    """
    )
