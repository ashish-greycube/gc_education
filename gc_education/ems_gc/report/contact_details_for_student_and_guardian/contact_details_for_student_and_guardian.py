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
with fn as
(
    select ROW_NUMBER() OVER(PARTITION BY parent ORDER BY tsg.idx) rn, 
    tsg.parent , tsg.guardian , tsg.guardian_name , tsg.relation ,
    tg.mobile_number , tg.email_address , tg.alternate_number
    from `tabStudent Guardian` tsg
    inner join tabGuardian tg on tg.name = tsg.guardian 
)
    select 
        tpe.academic_year , tpe.academic_term , 
        tpe.program , tpe.student_batch_name , 
        ts.g_r_number , tsgs.group_roll_number , tpe.student_name ,
        ts.student_mobile_number student_mobile_no , ts.student_email_id ,
        CONCAT_WS(', ', address_line_1, address_line_2, city, state ) address ,
        if(tsgs.active,'Active','Inactive') student_group_status ,
        if(ts.enabled,'Enabled','Disabled') student_status ,
        fn.guardian_name guardian1_name,
        fn.relation relation_with_guardian1, 
        fn.mobile_number guardian1_mobile_no, 
        fn.email_address guardian1_email_id, 
        fn.alternate_number guardian1_alternate_no,
        gr2.guardian_name guardian2_name,
        gr2.relation relation_with_guardian2, 
        gr2.mobile_number guardian2_mobile_no, 
        gr2.email_address guardian2_email_id, 
        gr2.alternate_number guardian2_alternate_no
    from tabStudent ts 
    inner join `tabProgram Enrollment` tpe on tpe.student = ts.name 
    inner join `tabStudent Group` tsg on tsg.program = tpe.program and tsg.academic_term = tpe.academic_term 
    inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = ts.name 
    left outer join fn on fn.parent = ts.name and fn.rn = 1
    left outer join fn gr2 on gr2.parent = ts.name and gr2.rn = 2	
    {conditions}
    order by tpe.program , tpe.student_batch_name , tsgs.group_roll_number , ts.g_r_number 
        limit 20
    """.format(
            conditions=get_conditions(filters)
        ),
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

    return conditions and " where " + " and ".join(conditions) or ""


def get_columns():
    return csv_to_columns(
        """
        Academic Year,academic_year,,,150
        Academic Term,academic_term,,,150
        Class,program,,,120
        Division,student_batch_name,,,120
        GR No.,g_r_number,,,90
        Roll No.,group_roll_number,,Int,90
        Name,student_name,,,290
        Student Status,student_status,,,120
        Class Status,student_group_status,,,120
        Student Mobile No,student_mobile_no,,,120 
        Student Email Id,student_email_id,,,120
        Student Address,address,,,120
        Guardian1 Name,guardian1_name,,,120
        Relation with Guardian1,relation_with_guardian1,,,120
        Guardian1 Mobile No,guardian1_mobile_no,,,120
        Guardian1 Email Id,guardian1_email_id,,,120
        Guardian1 Alternate No,guardian1_alternate_no,,,120
        Guardian2 Name,guardian2_name,,,120
        Relation with Guardian2,relation_with_guardian2,,,120
        Guardian2 Mobile No,guardian2_mobile_no, ,,120
        Guardian2 Email Id,guardian2_email_id,,,120
        Guardian2 Alternate No,guardian2_alternate_no,,,120
    """
    )
