// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Class List"] = {
	"filters": [
		{ "label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link", "options": "Academic Year", },
		{ "label": "Academic Term", "fieldname": "academic_term", "fieldtype": "Link", "options": "Academic Term", },
		{ "label": "Program", "fieldname": "program", "fieldtype": "Link", "options": "Program", },
		{ "label": "Batch", "fieldname": "batch", "fieldtype": "Link", "options": "Student Batch Name", },
	]
};
