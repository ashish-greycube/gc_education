# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.accounts.party import get_party_account, get_party_bank_account
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.doctype.payment_request.payment_request import PaymentRequest
from erpnext.accounts.doctype.payment_entry.payment_entry import (
    get_company_defaults,
    get_payment_entry,
)
from frappe.utils import nowdate
from payments.utils import get_payment_gateway_controller
from frappe.utils import flt, get_url, nowdate
import json
import urllib.parse


class GCPaymentRequest(PaymentRequest):
    """
    override payment_request of erpnext
    """

    def get_fees_description(self, fees_name):
        for d in frappe.db.sql(
            """
                    select 
                        student `Student Id` , 
                        g_r_number_cf `Student GR No.`,
                        student_name `Student Name` , 
                        concat(program, '/', student_batch) `Class/Division` ,
                        academic_year `Academic Year` , 
                        academic_term `Academic Term` 
                    from tabFees tf 
                    where name = %s 
                """,
            (fees_name),
            as_dict=True,
        ):
            return d

    def get_payment_url(self):
        """
        Override erpnext fn to send student details in description to razorpay
        """
        if self.reference_doctype != "Fees":
            return super(GCPaymentRequest, self).get_payment_url()

        # custom code to set description in razorpay options.. see razorpay_checkout.js
        data = frappe.db.get_value(
            self.reference_doctype, self.reference_name, ["student_name"], as_dict=1
        )

        fees_description = self.get_fees_description(self.reference_name) or {}
        student_name = fees_description.get("Student Name")
        description = ", ".join(
            ["{}:{}".format(k, fees_description[k]) for k in fees_description]
        )

        amount = flt(self.grand_total, self.precision("grand_total"))
        payment_options = {
            "amount": amount,
            "title": "{}-{}".format(amount, student_name),
            "description": description,
            "reference_doctype": "Payment Request",
            "reference_docname": self.name,
            "payer_email": self.email_to or frappe.session.user,
            "payer_name": student_name,
            "order_id": self.name,
            "currency": self.currency,
        }

        controller = get_payment_gateway_controller(self.payment_gateway)
        controller.validate_transaction_currency(self.currency)

        if hasattr(controller, "validate_minimum_transaction_amount"):
            controller.validate_minimum_transaction_amount(
                self.currency, self.grand_total
            )

        return controller.get_payment_url(**payment_options)

    def create_payment_entry(self, submit=True):
        """Set Branch, Party Type, Party Name, Mode of Payment for Fees"""
        if not self.reference_doctype == "Fees":
            return super(PaymentRequest, self).create_payment_entry(submit=submit)

        frappe.flags.ignore_account_permission = True

        ref_doc = frappe.get_doc(self.reference_doctype, self.reference_name)

        party_account = ref_doc.receivable_account

        party_account_currency = ref_doc.get(
            "party_account_currency"
        ) or get_account_currency(party_account)

        bank_amount = self.grand_total
        if (
            party_account_currency == ref_doc.company_currency
            and party_account_currency != self.currency
        ):
            party_amount = ref_doc.base_grand_total
        else:
            party_amount = self.grand_total

        payment_type = "Receive" if party_amount > 0 else None

        payment_entry = get_payment_entry(
            self.reference_doctype,
            self.reference_name,
            party_type="Student",
            payment_type=payment_type,
            party_amount=party_amount,
            bank_account=self.payment_account,
            bank_amount=bank_amount,
        )

        payment_entry.update(
            {
                "reference_no": self.name,
                "reference_date": nowdate(),
                "remarks": "Payment Entry against {0} {1} via Payment Request {2}".format(
                    self.reference_doctype, self.reference_name, self.name
                ),
            }
        )

        # set party name from Student, set branch from Fees, mode_of_payment from branch
        payment_entry.update(
            {
                "branch": ref_doc.get("branch"),
                "mode_of_payment": frappe.db.get_value(
                    "Branch", ref_doc.get("branch"), "mode_of_payment_cf"
                ),
            }
        )

        if payment_entry.difference_amount:
            company_details = get_company_defaults(ref_doc.company)

            payment_entry.append(
                "deductions",
                {
                    "account": company_details.exchange_gain_loss_account,
                    "cost_center": company_details.cost_center,
                    "amount": payment_entry.difference_amount,
                },
            )

        if submit:
            payment_entry.insert(ignore_permissions=True)
            payment_entry.submit()

        # db_set party_name as frappe sets it to name by default
        payment_entry.db_set(
            "party_name", frappe.db.get_value("Student", self.party, "student_name")
        )

        return payment_entry

    def on_submit(self):
        """set payment url in Fees to send Whatsapp notification"""
        super(GCPaymentRequest, self).on_submit()
        if self.payment_url:
            if self.reference_doctype == "Fees":
                frappe.enqueue(
                    set_payment_url_in_fees,
                    docname=self.reference_name,
                    payment_url=self.payment_url,
                )

    def set_as_cancelled(self):
        """unset payment url in Fees."""
        super(GCPaymentRequest, self).set_as_cancelled()
        if self.reference_doctype == "Fees":
            frappe.db.set_value("Fees", self.reference_name, "payment_url_cf", None)
            frappe.db.commit()


def set_payment_url_in_fees(docname, payment_url):
    frappe.db.set_value("Fees", docname, "payment_url_cf", payment_url)
