// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Class Teacher List"] = {

	"filters": [
		{ "label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link", "options": "Academic Year", },
		{ "label": "Academic Term", "fieldname": "academic_term", "fieldtype": "Link", "options": "Academic Term", },
		{
			"fieldname": "program",
			"label": __("Class List"),
			"fieldtype": "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Program', txt);
			}
		},
		{ "label": "Division", "fieldname": "batch", "fieldtype": "Link", "options": "Student Batch Name", },
	]
};
