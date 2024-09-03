from . import __version__ as app_version

app_name = "gc_education"
app_title = "GC Education"
app_publisher = "Greycube"
app_description = "Education Module Extensions"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gc_education/css/gc_education.css"
app_include_js = "/assets/gc_education/js/ems_gc.js"

# include js, css files in header of web template
# web_include_css = "/assets/gc_education/css/gc_education.css"
# web_include_js = "/assets/gc_education/js/gc_education.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gc_education/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Payment Entry": "public/js/payment_entry.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "gc_education.utils.jinja_methods",
# 	"filters": "gc_education.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "gc_education.install.before_install"
# after_install = "gc_education.install.after_install"
after_migrate = "gc_education.install.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "gc_education.uninstall.before_uninstall"
# after_uninstall = "gc_education.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gc_education.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Payment Request": "gc_education.overrides.payment_request.GCPaymentRequest"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Student Applicant": {
        "validate": "gc_education.ems_gc.controllers.doc_events.validate_student_applicant"
    },
    "Payment Ledger Entry": {
        "on_update": "gc_education.ems_gc.controllers.doc_events.on_update_payment_ledger_entry"
    },
    "Payment Request": {
        "validate": "gc_education.ems_gc.controllers.doc_events.validate_payment_request"
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "0 18 * * *": [
        "gc_education.ems_gc.controllers.attendance.sync_user_attendance_events",
    ],
    # 	"all": [
    # 		"gc_education.tasks.all"
    # 	],
    # 	"daily": [
    # 		"gc_education.tasks.daily"
    # 	],
    # 	"hourly": [
    # 		"gc_education.tasks.hourly"
    # 	],
    # 	"weekly": [
    # 		"gc_education.tasks.weekly"
    # 	],
    # 	"monthly": [
    # 		"gc_education.tasks.monthly"
    # 	],
}

# Testing
# -------

# before_tests = "gc_education.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    # "frappe.desk.doctype.event.event.get_events": "gc_education.event.get_events"
    "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry": "gc_education.overrides.override_whitelisted.get_payment_entry",
    # "erpnext.accounts.doctype.payment_request.payment_request.make_payment_request": "gc_education.overrides.override_whitelisted.make_payment_request",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gc_education.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"gc_education.auth.validate"
# ]
jinja = {"methods": ["gc_education.ems_gc.print_format.get_print_context"]}
