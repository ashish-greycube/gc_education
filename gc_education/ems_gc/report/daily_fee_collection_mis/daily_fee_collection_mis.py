# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report import csv_to_columns
import pandas
import numpy as np


def execute(filters=None):
    return get_data(filters)


def get_data(filters):
    data = frappe.db.sql(
        """
        select 
            tpe.name ,
            tpe.posting_date , tpe.paid_amount , tpe.company , 
            tpe.branch , tpe.mode_of_payment , tpe.party ,
            tpe.reference_no , tpe.reference_date , tpe.cost_center , 
            enr.program class, enr.student_batch_name division ,
            enr.academic_year , enr.academic_term 
        from `tabPayment Entry` tpe
            inner join `tabProgram Enrollment` enr on enr.student = tpe.party
    {cond}
    """.format(
            cond=get_conditions(filters)
        ),
        filters,
        as_dict=True,
    )

    if not data:
        return [], []

    df = pandas.DataFrame.from_records(data)
    df1 = pandas.pivot_table(
        df,
        index=[
            "academic_year",
            "academic_term",
            "company",
            "mode_of_payment",
        ],
        values=["paid_amount"],
        columns=["branch"],
        fill_value=0,
        margins=True,
        margins_name="Total",
        aggfunc="sum",
        dropna=True,
    )
    df1.drop(index="Total", axis=0)
    df1.columns = df1.columns.to_series().str[1]
    df2 = df1.reset_index()

    columns = get_columns()

    for col in df1.columns.to_list():
        columns += [
            dict(label=col, fieldname=col, fieldtype="Currency", width=140),
        ]

    # columns[-1]["label"] = "Total"

    out = []
    for d in df2.to_dict("records"):
        out.append({k: v for k, v in d.items() if v})

    out[-1]["bold"] = 1

    return columns, out


def get_columns():
    return csv_to_columns(
        """
    Organization,company,,,245
    Academic Year,academic_year,,,160
    Academic Term,academic_term,,,160
    Mode Of Payment,mode_of_payment,,,150
    """
    )


def get_conditions(filters):
    conditions = ["tpe.docstatus = 1"]
    if filters.get("academic_year"):
        conditions.append(" enr.academic_year = %(academic_year)s")
    if filters.get("academic_term"):
        conditions.append(" enr.academic_term = %(academic_term)s")
    if filters.get("program"):
        conditions.append(" enr.program = %(program)s")
    if filters.get("batch"):
        conditions.append(" enr.student_batch_name = %(batch)s")
    if filters.get("from_date"):
        conditions.append("tpe.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("tpe.posting_date <= %(to_date)s")

    return conditions and " where " + " and ".join(conditions) or ""
