// Copyright (c) 2023, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Admission Applicant Detail"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    ems_gc.report_filters["program"],
    {
      fieldname: "applicant",
      label: __("Student Applicant"),
      fieldtype: "Link",
      options: "Student Applicant",
    },
  ],
};
