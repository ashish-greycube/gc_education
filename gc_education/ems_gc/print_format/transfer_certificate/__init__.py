# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
import pendulum
from gc_education.ems_gc.print_format import date_in_words


def get_print_context(**args):
    ctx = frappe._dict()
    doc = args.get("doc", {})
    ctx["date_of_birth_in_words"] = date_in_words(doc.get("date_of_birth")) or ""
    return ctx
