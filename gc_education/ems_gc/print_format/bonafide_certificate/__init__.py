# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
import pendulum
from gc_education.ems_gc.print_format import date_in_words


def get_print_context(**args):
    ctx = frappe._dict()

    doc = args.get("doc", {})

    if doc:

        for d in frappe.db.sql(
            """
        with fn1 as
        (
            select 
            ROW_NUMBER() OVER(PARTITION BY student order by enrollment_date) rn, 
            student , academic_year , program 
            from `tabProgram Enrollment` tpe
            where tpe.docstatus = 1
        ),
        fn2 as
        (
            select 
            ROW_NUMBER() OVER(PARTITION BY student order by enrollment_date desc) rn, 
            student , academic_year , program 
            from `tabProgram Enrollment` tpe
            where tpe.docstatus = 1
        )
        select 
            name , title , g_r_number , caste , date_of_birth , birth_place , birth_state ,
            fn1.academic_year from_year , fn1.program from_program ,
            fn2.academic_year to_year , fn2.program to_program
        from tabStudent ts
        inner join fn1 on fn1.student = ts.name and fn1.rn = 1
        inner join fn2 on fn2.student = ts.name and fn2.rn = 1
        where ts.name = %s
        """,
            (doc.get("student"),),
            as_dict=True,
        ):
            d["date_of_birth_in_words"] = date_in_words(d.date_of_birth)
            ctx.update(d)

    return ctx
