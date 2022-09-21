// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

const copy_columns = [
  "Student Mobile No",
  "Student Email Id",
  "Guardian1 Mobile No",
  "Guardian1 Email Id",
  "Guardian2 Mobile No",
  "Guardian2 Email Id",
];

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
      options: "\n" + copy_columns.join("\n"),
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
        return m[frappe.scrub(col) || null];
      });
      data = data.filter((n) => n);
      frappe.utils.copy_to_clipboard(data);
    });
  },
};
