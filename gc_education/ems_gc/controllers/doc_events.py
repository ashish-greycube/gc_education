# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe.email.doctype.notification.notification import evaluate_alert

from erpnext.accounts.doctype.payment_request.payment_request import (
    get_gateway_details,
    get_dummy_message,
)


def validate_student_applicant(doc, method):
    for d in ["Father", "Mother"]:
        if [x for x in doc.guardians if x.relation == d]:
            continue

        relation = frappe.scrub(d)
        guardian = frappe.get_doc(
            {
                "doctype": "Guardian",
                "designation": "Father",
                "annual_income": doc.get(f"{relation}_annual_income_cf"),
                "education": doc.get(f"{relation}_education_cf"),
                "email_address": doc.get(f"{relation}_mail_cf"),
                "mobile_number": doc.get(f"{relation}_mobile_cf"),
                "guardian_name": doc.get(f"{relation}_name_cf"),
                "name_of_firm": doc.get(f"{relation}_name_of_firm_cf"),
                "occupation": doc.get(f"{relation}_occupation_cf"),
            }
        ).insert()

        doc.append(
            "guardians",
            {
                "guardian": guardian.name,
                "guardian_name": guardian.guardian_name,
                "relation": d,
            },
        )


def on_update_payment_ledger_entry(doc, method):
    """
    Send notification for Fees Paid: On Fees Paid-Email
    outstanding_amount in Fees is updated through db.set_value
    and value_changed event is not fired, so Custom event is used
    Create a notification with name = 'On Fees Paid-Email' and event = 'Custom'
    """
    if (
        doc.against_voucher_type == "Fees"
        and doc.flags.update_outstanding == "Yes"
        and not frappe.flags.is_reverse_depr_entry
    ):
        if (
            frappe.db.get_value(
                doc.against_voucher_type, doc.against_voucher_no, "outstanding_amount"
            )
            == 0
        ):
            try:
                evaluate_alert(
                    frappe.get_doc(doc.against_voucher_type, doc.against_voucher_no),
                    "On Fees Paid-Email",
                    "Custom",
                )
            except Exception:
                pass


def validate_payment_request(doc, method):
    """set gateway account based on Branch for Fees."""
    if not doc.reference_doctype == "Fees":
        return
    for d in frappe.db.sql(
        """
        select 
            tb.payment_gateway_account_cf payment_gateway_account , mode_of_payment_cf
        from tabFees tf 
        inner join tabBranch tb on tb.name = tf.branch 
        where tf.name = %s
    """,
        (doc.reference_name,),
        as_dict=True,
    ):
        d["order_type"] = ""
        gateway_account = get_gateway_details(d)
        doc.payment_gateway_account = gateway_account.get("name")
        doc.payment_gateway = gateway_account.get("payment_gateway")
        doc.payment_account = gateway_account.get("payment_account")
        doc.payment_channel = gateway_account.get("payment_channel")
        doc.message = gateway_account.get("message") or get_dummy_message(
            frappe.get_doc("Fees", doc.reference_name)
        )
