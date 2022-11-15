# -*- coding: utf-8 -*-
# Copyright (c) 2022, Greycube and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.accounts.doctype.payment_request.payment_request import (
    get_gateway_details,
    get_amount,
    get_existing_payment_request_amount,
    get_dummy_message,
    make_payment_request as _make_payment_request,
)
from erpnext.accounts.party import get_party_account, get_party_bank_account
from erpnext.accounts.doctype.payment_entry.payment_entry import (
    get_payment_entry as _get_payment_entry,
)


@frappe.whitelist()
def get_payment_entry(
    dt,
    dn,
    party_amount=None,
    bank_account=None,
    bank_amount=None,
    party_type=None,
    payment_type=None,
):
    pe = _get_payment_entry(
        dt, dn, party_amount, bank_account, bank_amount, party_type, payment_type
    )
    if not dt in "Fees":
        return pe
    pe.party_name = frappe.db.get_value(
        "Student", frappe.db.get_value("Fees", dn, "student"), "title"
    )
    return pe


@frappe.whitelist(allow_guest=True)
def make_payment_request(**args):
    """Make payment request"""

    # frappe.throw("u")

    # Use ErpNext method if not Fees
    if not args.get("dt") == "Fees":
        return _make_payment_request(**args)

    args = frappe._dict(args)
    ref_doc = frappe.get_doc(args.dt, args.dn)
    if args.dt == "Fees":
        for d in frappe.db.sql(
            """
                select 
                    tb.payment_gateway_account_cf , mode_of_payment_cf
                from tabFees tf 
                inner join tabBranch tb on tb.name = tf.branch 
                where tf.name = %s
            """,
            (args.dn,),
            as_dict=True,
        ):
            args["payment_gateway_account"] = d["payment_gateway_account_cf"]
            args["mode_of_payment"] = d["mode_of_payment_cf"]

    gateway_account = get_gateway_details(args) or frappe._dict()

    grand_total = get_amount(ref_doc, gateway_account.get("payment_account"))
    if args.loyalty_points and args.dt == "Sales Order":
        from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
            validate_loyalty_points,
        )

        loyalty_amount = validate_loyalty_points(ref_doc, int(args.loyalty_points))
        frappe.db.set_value(
            "Sales Order",
            args.dn,
            "loyalty_points",
            int(args.loyalty_points),
            update_modified=False,
        )
        frappe.db.set_value(
            "Sales Order",
            args.dn,
            "loyalty_amount",
            loyalty_amount,
            update_modified=False,
        )
        grand_total = grand_total - loyalty_amount

    bank_account = (
        get_party_bank_account(args.get("party_type"), args.get("party"))
        if args.get("party_type")
        else ""
    )

    existing_payment_request = None
    if args.order_type == "Shopping Cart":
        existing_payment_request = frappe.db.get_value(
            "Payment Request",
            {
                "reference_doctype": args.dt,
                "reference_name": args.dn,
                "docstatus": ("!=", 2),
            },
        )

    if existing_payment_request:
        frappe.db.set_value(
            "Payment Request",
            existing_payment_request,
            "grand_total",
            grand_total,
            update_modified=False,
        )
        pr = frappe.get_doc("Payment Request", existing_payment_request)
    else:
        if args.order_type != "Shopping Cart":
            existing_payment_request_amount = get_existing_payment_request_amount(
                args.dt, args.dn
            )

            if existing_payment_request_amount:
                grand_total -= existing_payment_request_amount

        pr = frappe.new_doc("Payment Request")
        pr.update(
            {
                "payment_gateway_account": gateway_account.get("name"),
                "payment_gateway": gateway_account.get("payment_gateway"),
                "payment_account": gateway_account.get("payment_account"),
                "payment_channel": gateway_account.get("payment_channel"),
                "payment_request_type": args.get("payment_request_type"),
                "currency": ref_doc.currency,
                "grand_total": grand_total,
                "mode_of_payment": args.mode_of_payment,
                "email_to": args.recipient_id or ref_doc.owner,
                "subject": _("Payment Request for {0}").format(args.dn),
                "message": gateway_account.get("message") or get_dummy_message(ref_doc),
                "reference_doctype": args.dt,
                "reference_name": args.dn,
                "party_type": args.get("party_type") or "Customer",
                "party": args.get("party") or ref_doc.get("customer"),
                "bank_account": bank_account,
            }
        )

        if args.order_type == "Shopping Cart" or args.mute_email:
            pr.flags.mute_email = True

        pr.insert(ignore_permissions=True)
        if args.submit_doc:
            pr.submit()

    if args.order_type == "Shopping Cart":
        frappe.db.commit()
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = pr.get_payment_url()

    if args.return_doc:
        return pr

    return pr.as_dict()
