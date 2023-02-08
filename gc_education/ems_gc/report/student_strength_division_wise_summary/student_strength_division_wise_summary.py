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
        Class,class,,,250
        Division,class_division,,,250
		Total,strength,Int,,200
    """
    )


def get_data(filters):
    data = frappe.db.sql(
        """
	select 
		t.academic_year , t.academic_term , t.class , t.class_division , 
        t.sort_order , count(*) strength
	from 
    (
		select 
        tpe.academic_year , tpe.academic_term , 
        tpe.program class, tpe.student_batch_name division, 
        concat( tpe.program, ' - ', tpe.student_batch_name) class_division, 
        ts.g_r_number , tsgs.group_roll_number , ts.title ,
        case tsgs.active when 1 then 'Active' else 'Inactive' end class_status ,
        case tsg.disabled when 1 then 'Disabled' else 'Enabled' end status ,
        if(tpr.sort_order_cf,tpr.sort_order_cf,ascii(tpr.name)*100) sort_order
		from tabStudent ts 
		inner join `tabProgram Enrollment` tpe on tpe.docstatus = 1 and tpe.student = ts.name 
        inner join `tabProgram` tpr on tpr.name = tpe.program
		inner join `tabStudent Group` tsg on tsg.program = tpe.program 
			and tsg.academic_term = tpe.academic_term 
		inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name 
			and tsgs.student = ts.name 
		{cond}
	) t
	group by academic_year , academic_term , sort_order, class , class_division
    order by sort_order , class , division 
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
        conditions.append(" tpe.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" tpe.academic_term = %(academic_term)s")
    if filters.get("batch"):
        conditions.append(" tpe.student_batch_name = %(batch)s")
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
