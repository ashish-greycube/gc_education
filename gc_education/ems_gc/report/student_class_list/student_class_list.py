# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns
from frappe.utils import cstr


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return csv_to_columns(
        """
        Academic Year,academic_year,,,150
        Academic Term,academic_term,,,150
        Class,program,,,120
        Division,student_batch_name,,120
        GR No.,g_r_number,,,120
        Roll No.,group_roll_number,,Int,120
        Student Status,student_status,,,120
        Class Status,class_status,,,120
        Name,title,,,250
        LC Number,leaving_certificate_number,,,130
    """
    )


def get_data(filters):
    data = frappe.db.sql(
        """
    select 
        tpe.academic_year , tpe.academic_term , 
        tpe.program , tpe.student_batch_name , 
        ts.g_r_number , tsgs.group_roll_number , ts.title ,
        case tsgs.active when 1 then 'Active' else 'Inactive' end class_status ,
        case ts.enabled when 1 then 'Enabled' else 'Disabled' end student_status ,
        ts.leaving_certificate_number 
    from tabStudent ts 
    inner join `tabProgram Enrollment` tpe on tpe.student = ts.name 
    inner join `tabStudent Group` tsg on tsg.program = tpe.program and tsg.academic_term = tpe.academic_term 
    inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = ts.name 
    {cond}
    order by tpe.program , tpe.student_batch_name , tsgs.group_roll_number , ts.g_r_number 
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
    if filters.get("academic_year"):
        conditions.append(" tpe.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" tpe.academic_term = %(academic_term)s")
    if filters.get("program"):
        conditions.append(" tpe.program = %(program)s")
    if filters.get("batch"):
        conditions.append(" tpe.student_batch_name = %(batch)s")
    if filters.get("student_status"):
        conditions.append(
            "ts.enabled = {}".format(
                filters.get("student_status") == "Enabled" and 1 or 0
            )
        )
    return conditions and " where " + " and ".join(conditions) or ""
