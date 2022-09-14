
// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Student Records General Register"] = {
	"filters": [
		{
			"label": "Student Status", "fieldname": "student_status",
			"fieldtype": "Select", "options": "All\nEnabled\nDisabled",
			"default": "Enabled",
		},
		{
			"fieldname": "as_on_date",
			"label": __("As on Date (Exclude students with Leaving Date less than selected date)"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	]
};
