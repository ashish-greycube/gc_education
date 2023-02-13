// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

const copy_columns = {
  "Student Mobile No": "student_mobile_no",
  "Student Email Id": "student_email_id",
  "Guardian1 Mobile No": "g1_mobile_number",
  "Guardian1 Email Id": "g1_email_address",
  "Guardian2 Mobile No": "g2_mobile_number",
  "Guardian2 Email Id": "g2_email_address",
};

frappe.query_reports["Contact Details for Student and Guardian"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    ems_gc.report_filters["department"],
    ems_gc.report_filters["program"],
    ems_gc.report_filters["batch"],
    {
      label: "Copy Column",
      fieldname: "column_to_copy",
      fieldtype: "Select",
      options: "\n" + Object.keys(copy_columns).join("\n"),
      on_change: function () {
        // do nothing
      },
    },
    ems_gc.report_filters["student_status"],
  ],
  onload: function (report) {
    report.page.add_inner_button("Copy Column", () => {
      let col = frappe.query_report.get_filter_value("column_to_copy");
      if (!col) {
        frappe.throw("Please select the column to copy.");
      }
      let data = frappe.query_report.data.map((m) => {
        return m[copy_columns[col] || null];
      });
      data = data.filter((n) => n);
      frappe.utils.copy_to_clipboard(data);
    });
  },
};
