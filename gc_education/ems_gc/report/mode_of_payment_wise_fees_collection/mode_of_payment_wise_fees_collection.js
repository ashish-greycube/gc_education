// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Mode Of Payment-wise Fees Collection"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    {
      fieldname: "from_date",
      label: __("From Date (Payment Entry Posting Date)"),
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1,
    },
    {
      fieldname: "to_date",
      label: __("To Date (Payment Entry Posting Date)"),
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1,
    },
  ],
  formatter: function (value, row, column, data, default_formatter) {
    value = default_formatter(value, row, column, data);
    if (data && data.bold) {
      value = value.bold();
    }
    return value;
  },
  onload: function (report) {
    frappe.db.get_value(
      "Academic Year",
      frappe.defaults.get_default("academic_year"),
      ["year_start_date"],
      (r) => {
        report.set_filter_value("from_date", r.year_start_date);
      }
    );
  },
};
