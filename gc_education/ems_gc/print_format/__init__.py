# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
import pendulum
import os


def get_print_context(**args):
    if args.get("doc", {}).get("doctype", "") == "Fees":
        return get_fees_detail(**args)

    print_format = frappe.scrub(args.get("print_format", ""))

    if print_format:
        if os.path.exists(os.path.join(os.path.dirname(__file__), print_format)):
            module = frappe.get_module(
                f"gc_education.ems_gc.print_format.{print_format}"
            )
            return getattr(
                module,
                "get_print_context",
            )(**args)

    return {}


def date_in_words(dt):
    dt = pendulum.from_format(dt.strftime("%Y-%m-%d"), "YYYY-MM-DD")
    return dt.format("Do of MMM") + " " + frappe.unscrub(frappe.utils.in_words(dt.year))


def get_fees_detail(**args):
    for d in frappe.db.sql(
        """
    select 
        tpr.mode_of_payment , tpe.reference_no , tpe.reference_date , 'student bank ?' bank
    from `tabPayment Entry Reference` tper
    inner join `tabPayment Entry` tpe on tpe.name = tper.parent
    left outer join `tabPayment Request` tpr on tpr.name = tper.reference_name
    where tper.reference_doctype  = 'Fees' and tper.reference_name = %s
    limit 1
    """,
        (args.get("doc", {}).get("name", "")),
        as_dict=True,
    ):
        return d
