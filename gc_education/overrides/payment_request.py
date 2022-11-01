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


class GCPaymentRequest(PaymentRequest):

    # override payment_request.py
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
                "party_name": frappe.db.get_value("Student", self.party, "title"),
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

        return payment_entry
