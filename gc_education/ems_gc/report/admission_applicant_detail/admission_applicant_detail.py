# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns
import pandas
import numpy as np


def execute(filters=None):
    return get_columns(), get_data(filters)


def get_data(filters):
    data = frappe.db.sql(
        """
        select tsa.name , tsa.program , tsa.application_status ,
            CONCAT_WS(' ', first_name , middle_name , last_name ) student_name ,
            tsa.date_of_birth ,
            -- father
            tsg1.guardian_name fathers_name ,  
            tg1.occupation fathers_occupation ,
            tg1.name_of_firm fathers_name_of_firm ,
            tg1.annual_income fathers_annual_income ,
            tg1.are_you_ex_student_of_this_school father_ex ,
            if(tg1.are_you_ex_student_of_this_school = 'Yes', 
                tg1.year_of_admission_and_passing,'') fathers_ex ,
            tg1.education fathers_education ,
            tg1.mobile_number fathers_mobile_number ,
            -- mother
            tsg2.guardian_name mothers_name ,
            tg2.occupation mothers_occupation ,
            tg2.name_of_firm mothers_name_of_firm ,
            tg2.annual_income mothers_annual_income ,
            if(tg2.are_you_ex_student_of_this_school = 'Yes', 
                tg2.year_of_admission_and_passing,'') mothers_ex ,
            tg2.education mothers_education ,
            tg2.mobile_number mothers_mobile_number ,
            sib.siblings
        from `tabStudent Applicant` tsa 
        left outer join `tabStudent Guardian` tsg1 on tsg1.parent = tsa.name
            and tsg1.relation = 'Father'
        left outer join tabGuardian tg1 on tg1.name = tsg1.guardian  
        left outer join `tabStudent Guardian` tsg2 on tsg2.parent = tsa.name
            and tsg2.relation = 'Mother'	
        left outer join tabGuardian tg2 on tg2.name = tsg2.guardian 
        left outer join (
            select parent, 
            	GROUP_CONCAT(
                    CONCAT_WS(' ', full_name, 
                        if(nullif(gender,'') is not null,concat('(',left(gender,1),')'),''), 
                        program)
                ) siblings
            from `tabStudent Sibling`  
            group by parent 
        ) sib on sib.parent = tsa.name
    {cond}
    """.format(
            cond=get_conditions(filters)
        ),
        filters,
        as_dict=True,
    )

    return data


def get_columns():
    return csv_to_columns(
        """
    Applicant,name,Link,Student Applicant,,130
    Status,application_status,,,100
    Name of the Student,student_name,,,250
    Program,program,Link,Program,180
    Date Of Birth,date_of_birth,Date,,130
    Father Name,fathers_name,,,130
    Father Occupation,fathers_occupation,,,130
    Name of firm,fathers_name_of_firm,,,130
    Annual Income,fathers_annual_income,,,130
    Are you ex student of this school,fathers_ex,,,130
    Father Qualification,fathers_education,,,130
    Father Contact No,fathers_mobile_number,,,130
    Mother Name,mothers_name,,,130
    Mother Occupation,mothers_occupation,,,130
    Name of firm,mothers_name_of_firm,,,130
    Annual Income,mothers_annual_income,,,130
    Are you ex student of this school,mothers_ex,,,130
    Mother Qualification,mothers_education,,,130
    Mother Contact No,mothers_mobile_number,,,130
    Sibling,siblings,,,200
    """
    )


def get_conditions(filters):
    conditions = []
    if filters.get("academic_year"):
        conditions.append(" tsa.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" tsa.academic_term = %(academic_term)s")
    if filters.get("applicant"):
        conditions.append(" tsa.name = %(applicant)s")
    if filters.get("program"):
        lst = filters.program
        # to prevent SQL Injection
        programs = frappe.get_list("Program", pluck="name")
        conditions.append(
            "tsa.program in ({})".format(
                ",".join(["'%s'" % d for d in lst if d in programs])
            )
        )

    return conditions and " where " + " and ".join(conditions) or ""
