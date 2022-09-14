// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student-wise Fees Status"] = {

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
		{
			"fieldname": "from_date",
			"label": __("From Date (Fees Due Date)"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date (Fees Due Date)"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},

	],
	onload: function (report) {
		setTimeout(() => {
			$(`
			<div class="col-md-12">
				Note: From Date and To Date filter is applied on the fees due date.<br>
			</div>
			`).prependTo($('.report-footer'))
		}, 500);

	}
};
