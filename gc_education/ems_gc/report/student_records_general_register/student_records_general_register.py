# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    cols = []
    for d in csv_to_columns(
        """
		Register No,name,Link,Student,,130
        Students Name<>Aadhar Card No.,name_aadhar,,,250
        Father's Name<>Mother's Name,father_mother,,,250
		Name Of The School Last Attended<>UDISE No.,last_school,,,250
		Religion With Caste<>SC/ST/OBC/Others,religion_caste,,,250
		Date Of Birth,date,date_of_birth,Date,,180
		Place Of Birth,birth_place_name,,,180
		Date Of Admission (a)(b),joining_date,Date,,180
		Std. Of Admission,admission_class,,,180
		L.C. No.,leaving_certificate_number,,,180
		Date Of Issue L.C.,date_of_leaving,Date,,180
		Std. at The Time Of Leaving,leaving_class,,,180
		Signature,,,,180
    """
    ):
        col = dict(d)
        col.update({"label": col.get("label").replace("<>", "\n")})
        cols.append(col)
    return cols


def get_data(filters):
    data = frappe.db.sql(
        """
			with fn as
			(
				select 
					ROW_NUMBER() over(PARTITION BY student order by enrollment_date) rn, 
					program , student , enrollment_date 
				from `tabProgram Enrollment` tpe
			),
			fn2 as
			(
				select 
					ROW_NUMBER() over(PARTITION BY student order by enrollment_date desc) rn, 
					program , student , enrollment_date 
				from `tabProgram Enrollment` tpe
			)
			select ts.name , 
			concat_ws('\n',ts.title , ts.aadhaar_number ) name_aadhar,
			concat_ws('\n',pa.guardian_name, ma.guardian_name) father_mother ,
			CONCAT_WS('\n',ts.religion , concat_ws(', ',ts.caste_category , ts.caste)) religion_caste ,
			ts.date_of_birth , ts.birth_place_name , joining_date , 
			ts.date_of_leaving , ts.leaving_certificate_number ,
			fn.program admission_class , fn2.program leaving_class 
			from tabStudent ts 
			left outer join tabGuardian pa on pa.student_id = ts.name
			left outer join tabGuardian ma on ma.student_id = ts.name
			inner JOIN fn on fn.student = ts.name
			left outer join fn2 on fn2.student = ts.name and ts.date_of_leaving is not null
    {cond}
		order by ts.name
    """.format(
            cond=""
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
    if filters.get("program"):
        conditions.append(" tpe.program = %(program)s")
    if filters.get("batch"):
        conditions.append(" tpe.batch = %(batch)s")
    return conditions and "where" + " and ".join(conditions) or ""
