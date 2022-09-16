// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */


const copy_columns = [
	"Student Mobile No",
	"Student Email Id",
	"Guardian1 Mobile No",
	"Guardian1 Email Id",
	"Guardian2 Mobile No",
	"Guardian2 Email Id",
]



frappe.query_reports["Contact Details for Student and Guardian"] = {
	"filters": [
		{ "label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link", "options": "Academic Year", },
		{ "label": "Academic Term", "fieldname": "academic_term", "fieldtype": "Link", "options": "Academic Term", },
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Department', txt);
			}
		},
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
			label: "Copy Column",
			fieldname: "column_to_copy",
			fieldtype: "Select",
			options: "\n" + copy_columns.join("\n")
		},
		{
			"label": "Student Status", "fieldname": "student_status",
			"fieldtype": "Select", "options": "All\nEnabled\nDisabled",
			"default": "Enabled",
		},
	],
	onload: function (report) {
		report.page.add_inner_button("Copy Column", () => {
			let col = frappe.query_report.get_filter_value('column_to_copy');
			if (!col) {
				frappe.throw('Please select the column to copy.')
			}
			let data = frappe.query_report.data.map((m) => { return m[frappe.scrub(col) || null] });
			data = data.filter(n => n)
			frappe.utils.copy_to_clipboard(data);
		})
	}
};
