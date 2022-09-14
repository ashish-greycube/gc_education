# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_migrate(**args):

    custom_fields = {
        "Payment Entry": [
            dict(
                fieldtype="Link",
                options="Bank",
                fieldname="bank_name",
                label="Bank Name",
                insert_after="party_name",
                allow_on_submit=1,
            ),
        ],
    }
    create_custom_fields(custom_fields)
    frappe.db.commit()  # to avoid implicit-commit errors
