// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Mode Of Payment-wise Fees Collection"] = {
	"filters": [
		{ "label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link", "options": "Academic Year", },
		{ "label": "Academic Term", "fieldname": "academic_term", "fieldtype": "Link", "options": "Academic Term", },
		{
			"fieldname": "from_date",
			"label": __("From Date (Payment Entry Posting Date)"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date (Payment Entry Posting Date)"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	},
};
