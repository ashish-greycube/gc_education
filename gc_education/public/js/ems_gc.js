frappe.provide("ems_gc");

ems_gc.report_filters = {
  academic_year: {
    label: "Academic Year",
    fieldname: "academic_year",
    fieldtype: "Link",
    options: "Academic Year",
    default: frappe.defaults.get_default("academic_year"),
  },
  academic_term: {
    label: "Academic Term",
    fieldname: "academic_term",
    fieldtype: "Link",
    options: "Academic Term",
    default: frappe.defaults.get_default("academic_term"),
  },
  department: {
    fieldname: "department",
    label: __("Department"),
    fieldtype: "MultiSelectList",
    get_data: function (txt) {
      return frappe.db.get_link_options("Department", txt);
    },
  },
  program: {
    fieldname: "program",
    label: __("Class"),
    fieldtype: "MultiSelectList",
    get_data: function (txt) {
      return frappe.db.get_link_options("Program", txt);
    },
  },
  batch: {
    fieldname: "batch",
    label: __("Division"),
    fieldtype: "MultiSelectList",
    get_data: function (txt) {
      return frappe.db.get_link_options("Student Batch Name", txt);
    },
  },
  student_status: {
    label: "Student Status",
    fieldname: "student_status",
    fieldtype: "Select",
    options: "All\nEnabled\nDisabled",
    default: "Enabled",
  },
};
