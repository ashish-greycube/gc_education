# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from gc_education.ems_gc.report.student_wise_fees_status.student_wise_fees_status import (
    get_data,
)
from gc_education.ems_gc.report import csv_to_columns
from itertools import groupby
from operator import itemgetter


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    out = []

    for key, group in groupby(
        data,
        key=itemgetter("academic_year", "academic_term", "program", "division"),
    ):
        rows = list(group)
        for col in [
            "outstanding_amount",
            "paid_amount",
            "na_amount",
            "additional_amount",
            "exemption_amount",
            "grand_total",
        ]:
            rows[0].update({col: sum([d.get(col, 0) for d in rows])})

        if filters.get("show_pending_student_count"):
            rows[0].update(
                {"student_count": len([d for d in rows if d.get("outstanding_amount")])}
            )

        out.append(rows[0])

    return columns, out


def get_columns(filters):
    if filters.get("show_pending_student_count"):
        return csv_to_columns(
            """
            Academic Year,academic_year,,,150
            Academic Term,academic_term,,,150
            Class,program,,,120
            Division,division,,120
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
        Total Amount,grand_total,Currency,,130
        Additional Amount,additional_amount,Currency,,130
        Exemption Amount,exemption_amount,Currency,,130
        NA Amount,na_amount,Currency,,130
        Paid Amount,paid_amount,Currency,,130
        Pending Amount,outstanding_amount,Currency,,130
    """
    )
