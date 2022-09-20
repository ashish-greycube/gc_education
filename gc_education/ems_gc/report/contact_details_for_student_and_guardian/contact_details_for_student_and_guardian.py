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
    tg.mobile_number , tg.email_address , tg.alternate_number ,
    tg.annual_income , tg.occupation , tg.work_address , tg.name_of_firm ,
    tg.user ,tg.date_of_birth ,tg.education 
    from `tabStudent Guardian` tsg
    inner join tabGuardian tg on tg.name = tsg.guardian 
),
intr as (
    select parent , GROUP_CONCAT(interest) interests  from `tabGuardian Interest` tgi 
)
    select 
        tpe.academic_year , tpe.academic_term , tpr.department ,
        tpe.program , tpe.student_batch_name , 
        ts.g_r_number , tsgs.group_roll_number , tpe.student_name ,
        ts.student_mobile_number student_mobile_no , ts.student_email_id ,
        CONCAT_WS(', ', address_line_1, address_line_2, city, state ) address ,
        if(tsgs.active,'Active','Inactive') student_group_status ,
        if(ts.enabled,'Enabled','Disabled') student_status ,
        fn.guardian_name  g1_guardian_name,
        fn.education  g1_education,
        fn.occupation  g1_occupation,
        fn.work_address  g1_work_address,
        fn.annual_income  g1_annual_income,
        fn.name_of_firm  g1_name_of_firm,
        fn.user  g1_user,
        fn.date_of_birth  g1_date_of_birth,
        fn.alternate_number  g1_alternate_number,
        fn.mobile_number  g1_mobile_number,
        fn.email_address  g1_email_address,
        intr1.interests g1_interests,
        fn2.guardian_name  g2_guardian_name,
        fn2.education  g2_education,
        fn2.occupation  g2_occupation,
        fn2.work_address  g2_work_address,
        fn2.annual_income  g2_annual_income,
        fn2.name_of_firm  g2_name_of_firm,
        fn2.user  g2_user,
        fn2.date_of_birth  g2_date_of_birth,
        fn2.alternate_number  g2_alternate_number,
        fn2.mobile_number  g2_mobile_number,
        fn2.email_address  g2_email_address,
        intr2.interests g2_interests
    from tabStudent ts 
    inner join `tabProgram Enrollment` tpe on tpe.student = ts.name 
    inner join `tabProgram` tpr on tpr.name = tpe.program
    inner join `tabStudent Group` tsg on tsg.program = tpe.program and tsg.academic_term = tpe.academic_term 
    inner join `tabStudent Group Student` tsgs on tsgs.parent = tsg.name and tsgs.student = ts.name 
    left outer join fn on fn.parent = ts.name and fn.rn = 1
    left outer join fn fn2 on fn2.parent = ts.name and fn2.rn = 2	
    left outer join intr intr1 on intr1.parent = fn.guardian
    left outer join intr intr2 on intr2.parent = fn2.guardian
    {conditions}
    order by tpe.program , tpe.student_batch_name , tsgs.group_roll_number , ts.g_r_number 
    """.format(
            conditions=get_conditions(filters)
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
        Department,department,,,120
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
        Guardian1 Name,g1_guardian_name,,,120
        Guardian1 Mobile No,g1_mobile_number,,,120
        Guardian1 Email,g1_email_address,,,120
        Guardian1 Alt Number,g1_alternate_number,,,120
        Guardian1 Education,g1_education,,,120
        Guardian1 Occupation,g1_occupation,,,120
        Guardian1 Work Address,g1_work_address,,,120
        Guardian1 Annual Income,g1_annual_income,,,120
        Guardian1 Firm,g1_name_of_firm,,,120
        Guardian1 User,g1_user,,,120
        Guardian1 DoB,g1_date_of_birth,,,120        
        Guardian1 Interests,g1_interests,,,120
        Guardian2 Name,g2_guardian_name,,,120
        Guardian2 Mobile No,g2_mobile_number,,,120
        Guardian2 Email,g2_email_address,,,120
        Guardian2 Alt Number,g2_alternate_number,,,120
        Guardian2 Education,g2_education,,,120
        Guardian2 Occupation,g2_occupation,,,120
        Guardian2 Work Address,g2_work_address,,,120
        Guardian2 Annual Income,g2_annual_income,,,120
        Guardian2 Firm,g2_name_of_firm,,,120
        Guardian2 User,g2_user,,,120
        Guardian2 DoB,g2_date_of_birth,,,120
        Guardian2 Interests,g2_interests,,,120
    """
    )
