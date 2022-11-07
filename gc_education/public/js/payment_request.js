// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment Request", {
  refresh: function (frm) {
    if (
      frm.doc.payment_request_type == "Inward" &&
      frm.doc.payment_channel !== "Phone" &&
      in_list(["Initiated"], frm.doc.status) &&
      !frm.doc.__islocal &&
      frm.doc.docstatus == 1
    ) {
      frm.add_custom_button(__("Resend Payment Email"), function () {
        frappe.call({
          method:
            "erpnext.accounts.doctype.payment_request.payment_request.resend_payment_email",
          args: { docname: frm.doc.name },
          freeze: true,
          freeze_message: __("Sending"),
          callback: function (r) {
            if (!r.exc) {
              frappe.msgprint(__("Message Sent"));
            }
          },
        });
      });
    }
    //
  },
});
