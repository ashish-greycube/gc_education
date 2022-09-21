// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Class Teacher List"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    ems_gc.report_filters["department"],
    ems_gc.report_filters["program"],
    ems_gc.report_filters["batch"],
  ],
};
