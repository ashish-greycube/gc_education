// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Class List"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    ems_gc.report_filters["department"],
    ems_gc.report_filters["program"],
    ems_gc.report_filters["batch"],
    {
      fieldname: "as_on_date",
      label: __("As on Date"),
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1,
    },
    ems_gc.report_filters["student_status"],
  ],
  onload: function (report) {
    // set_options()
  },
};
