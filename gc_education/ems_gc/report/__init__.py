# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe


def csv_to_columns(csv_str):
    props = ["label", "fieldname", "fieldtype", "options", "width"]
    return [
        dict(zip(props, [x.strip() for x in col.split(",")]))
        for col in csv_str.split("\n")
        if col.strip()
    ]
