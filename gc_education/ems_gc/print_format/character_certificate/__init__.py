# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
import pendulum
from gc_education.ems_gc.print_format import date_in_words


def get_print_context(**args):
    ctx = frappe._dict()
    doc = args.get("doc", {})
    ctx["student_group_name"] = doc.get("student_group", "").split("/")[0] or ""
    return ctx
