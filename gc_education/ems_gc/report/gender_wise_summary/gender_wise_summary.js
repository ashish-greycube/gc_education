// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Gender-wise Summary"] = {
	"filters": [
		{ "label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link", "options": "Academic Year", },
		{ "label": "Academic Term", "fieldname": "academic_term", "fieldtype": "Link", "options": "Academic Term", },
		{
			"fieldname": "program",
			"label": __("Class"),
			"fieldtype": "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Program', txt);
			}
		},
		{
			"fieldname": "batch",
			"label": __("Division"),
			"fieldtype": "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Student Batch Name', txt);
			}
		},
		{
			"label": "Student Status", "fieldname": "student_status",
			"fieldtype": "Select", "options": "All\nEnabled\nDisabled",
			"default": "Enabled",
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
