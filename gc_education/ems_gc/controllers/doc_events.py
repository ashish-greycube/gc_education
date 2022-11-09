# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe.email.doctype.notification.notification import evaluate_alert


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
