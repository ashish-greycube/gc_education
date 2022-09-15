// Copyright (c) 2022, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Class List"] = {
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
			"fieldname": "as_on_date",
			"label": __("As on Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"label": "Student Status", "fieldname": "student_status",
			"fieldtype": "Select", "options": "All\nEnabled\nDisabled",
			"default": "Enabled",
		},

	],
	onload: function (report) {
		// set_options()
	}
};

// function set_options(params) {

// 	frappe.db.get_list("Program").then(o => {
// 		let class_filter = frappe.query_report.get_filter('class');

// 		let lst = o.map()
// 		class_filter.set_data(r.message);

// 		console.log(o)
// 	})

// 	frappe.call({
// 		method: "frappe.email.get_contact_list",
// 		args: { "txt": "ram" },
// 		callback: (r) => {
// 			console.log(r.message);
// 			class_filter.set_data(r.message);
// 		},
// 	});

	// ["recipients", "cc", "bcc"].forEach((field) => {
	// 	this.dialog.fields_dict[field].get_data = () => {
	// 		const data = this.dialog.fields_dict[field].get_value();
	// 		const txt = data.match(/[^,\s*]*$/)[0] || "";

	// 		frappe.call({
	// 			method: "frappe.email.get_contact_list",
	// 			args: { txt },
	// 			callback: (r) => {
	// 				this.dialog.fields_dict[field].set_data(r.message);
	// 			},
	// 		});
	// 	};
	// });
// }
