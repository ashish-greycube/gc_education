// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["House-wise Summary"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    ems_gc.report_filters["department"],
    ems_gc.report_filters["program"],
    ems_gc.report_filters["batch"],
    ems_gc.report_filters["student_status"],
  ],
  formatter: function (value, row, column, data, default_formatter) {
    value = default_formatter(value, row, column, data);
    if (data && data.bold) {
      value = value.bold();
    }
    return value;
  },
};
