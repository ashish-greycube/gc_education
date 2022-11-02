// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment Entry", {
  refresh: function (frm) {
    if (
      frm.is_new() &&
      frm.doc.party_type == "Student" &&
      frm.doc.payment_type == "Receive" &&
      !frm.doc.branch
    ) {
      if (
        (frm.doc.references || []).length ||
        frm.doc.references[0].reference_doctype == "Fees"
      ) {
        frappe.db
          .get_value("Fees", frm.doc.references[0].reference_name, ["branch"])
          .then(({ message }) => {
            frm.set_value("branch", message.branch);
          });
      }
    }
  },
});
