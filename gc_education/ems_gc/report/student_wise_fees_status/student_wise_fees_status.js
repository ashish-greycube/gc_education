// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student-wise Fees Status"] = {
  filters: [
    ems_gc.report_filters["academic_year"],
    ems_gc.report_filters["academic_term"],
    ems_gc.report_filters["department"],
    ems_gc.report_filters["program"],
    ems_gc.report_filters["batch"],
    {
      fieldname: "from_date",
      label: __("From Date (Fees Due Date)"),
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1,
    },
    {
      fieldname: "to_date",
      label: __("To Date (Fees Due Date)"),
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1,
    },
  ],
  onload: function (report) {
    frappe.db.get_value(
      "Academic Year",
      frappe.defaults.get_default("academic_year"),
      ["year_start_date"],
      (r) => {
        report.set_filter_value("from_date", r.year_start_date);
      }
    );

    setTimeout(() => {
      $(`
			<div class="col-md-12">
				Note: From Date and To Date filter is applied on the fees due date.<br>
			</div>
			`).prependTo($(".report-footer"));
    }, 500);
  },
};
