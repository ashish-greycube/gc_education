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
        Class,class,,,150
        Division,division,,,150
        Class Teacher,class_teacher_cf,,,250
        Employee ID,employee,Link,Employee,130
    """
    )


def get_data(filters):
    data = frappe.db.sql(
        """
		select 
			academic_year , academic_term , 
			program class, batch division, class_teacher_cf , te.name employee
		from `tabStudent Group` tsg 
		inner join tabInstructor ti on ti.name = tsg.class_teacher_cf 
		inner join tabEmployee te on te.name = ti.employee 
    {cond}
		order by program , batch 
    """.format(
            cond=get_conditions(filters)
        ),
        filters,
        as_dict=True,
    )
    data.append(
        {
            # "academic_year": "Total",
            "division": frappe.bold("Total "),
            "class_teacher_cf": frappe.bold(cstr(len(data))),
        }
    )
    return data


def get_conditions(filters):
    conditions = []
    if filters.get("academic_year"):
        conditions.append(" tsg.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" tsg.academic_term = %(academic_term)s")
    if filters.get("program"):
        conditions.append(" tsg.program = %(program)s")
    if filters.get("batch"):
        conditions.append(" tsg.batch = %(batch)s")
    return conditions and "where" + " and ".join(conditions) or ""
