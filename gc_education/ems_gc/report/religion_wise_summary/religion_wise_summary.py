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
        ts.name , ts.religion , ts.gender , tpe.program class, tpe.student_batch_name division
    from tabStudent ts 
    inner join `tabProgram Enrollment` tpe on tpe.student = ts.name 	
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
            "class",
            "division",
        ],
        values=["name"],
        columns=["religion", "gender"],
        fill_value=0,
        margins=True,
        margins_name="Total",
        aggfunc="count",
        dropna=True,
    )
    df1.drop(index="Total", axis=0)
    df1.columns = (
        df1.columns.to_series().str[1] + " (" + df1.columns.to_series().str[2] + ")"
    )
    df2 = df1.reset_index()

    columns = [
        dict(label="Class", fieldname="class", fieldtype="Data", width=160),
        dict(
            label="Division",
            fieldname="division",
            fieldtype="Data",
            width=160,
        ),
    ]

    for col in df1.columns.to_list():
        columns += [
            dict(label=col, fieldname=col, fieldtype="Int", width=140),
        ]

    columns[-1]["label"] = "Total"

    out = []
    for d in df2.to_dict("r"):
        out.append({k: v for k, v in d.items() if v})

    return columns, out


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
    return conditions and "where" + " and ".join(conditions) or ""
