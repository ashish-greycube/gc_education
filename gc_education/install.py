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
        "Branch": [
            dict(
                fieldtype="Link",
                options="Payment Gateway Account",
                fieldname="payment_gateway_account_cf",
                label="Payment Gateway Account",
                insert_after="branch",
            ),
        ],
        "Fees": [
            dict(
                fieldtype="Data",
                fieldname="payment_url_cf",
                label="Payment Url",
                read_only=1,
                hidden=1,
                translatable=0,
            ),
        ],
    }
    create_custom_fields(custom_fields)
    frappe.db.commit()  # to avoid implicit-commit errors
