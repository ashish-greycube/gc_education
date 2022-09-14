
// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Student Records General Register"] = {
	"filters": [
		{
			"label": "Student Status", "fieldname": "student_status",
			"fieldtype": "Select", "options": "\nEnabled\nDisabled",
			"default": "Enabled",
		},
	]
};
