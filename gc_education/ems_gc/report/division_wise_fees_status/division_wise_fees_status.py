# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report.student_wise_fees_status.student_wise_fees_status import (
    get_data,
)
from gc_education.ems_gc.report import csv_to_columns
from itertools import groupby
from operator import itemgetter
from frappe.desk.query_report import add_total_row


def execute(filters=None):
    _columns, data = get_data(filters)
    data = data[:-1]

    columns_to_total = [
        d["fieldname"]
        for d in _columns
        if isinstance(d, dict) and d.get("fieldtype") == "Currency"
    ]
    out = []

    for key, group in groupby(
        data,
        key=itemgetter(
            "academic_year", "academic_term", "program", "division", "description"
        ),
    ):
        rows = list(group)
        for col in columns_to_total:
            rows[0].update({col: sum([d.get(col, 0) for d in rows])})

        if filters.get("show_pending_student_count"):
            rows[0].update(
                {"student_count": len([d for d in rows if d.get("outstanding_amount")])}
            )

        out.append(rows[0])

    columns = get_columns(filters)
    if not filters.get("show_pending_student_count"):
        columns[5:5] = [d for d in _columns if isinstance(d, dict)]

    # fix for add_total_row: if i >= len(row):
    for row in out:
        row.update({str(x): x for x in range(len(columns) - len(row) + 1)})

    add_total_row(out, columns)
    return columns, out


def get_columns(filters):
    if filters.get("show_pending_student_count"):
        return csv_to_columns(
            """
            Academic Year,academic_year,,,150
            Academic Term,academic_term,,,150
            Class,program,,,120
            Division,division,,120
            Quarter,description,,,130
            Student Count,student_count,Int,,130
            Pending Amount,outstanding_amount,Currency,,130
        """
        )

    return csv_to_columns(
        """
        Academic Year,academic_year,,,150
        Academic Term,academic_term,,,150
        Class,program,,,120
        Division,division,,120
        Quarter,description,,,130
    """
    )
