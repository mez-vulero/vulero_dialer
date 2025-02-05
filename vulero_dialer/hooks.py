app_name = "vulero_dialer"
app_title = "Vulero Dialer"
app_publisher = "vulerotech"
app_description = "Dialer Modal for Ethiopia"
app_email = "mezmure.dawit@vulero.et"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vulero_dialer/css/vulero_dialer.css"
#app_include_js = "/assets/vulero_dialer/js/vulero_dialer.js"
app_include_js = [
	"vulero_dialer.bundle.js"
	]
on_login = [
    "vulero_dialer.config.call_log.fetch_and_process_call_logs", 
    "vulero_dialer.config.call_log.fetch_and_process_outgoing_call_logs",
    "vulero_dialer.config.call_log.fetch_and_process_offhour_logs",
    "vulero_dialer.config.call_log.fetch_and_process_missed_call_logs"
]
# include js, css files in header of web template
# web_include_css = "/assets/vulero_dialer/css/vulero_dialer.css"
# web_include_js = "/assets/vulero_dialer/js/vulero_dialer.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vulero_dialer/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"Lead" : "/assets/vulero_dialer/js/lead_call.js", "Opportunity" : "public/js/opportunity_call.js", "Customer" : "public/js/customer_call.js", "Contact" : "public/js/contact_call.js"}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vulero_dialer/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

website_route_rules = [
    {"from_route": "/vulero_dialer/<path:app_path>", "to_route": "vulero_dialer"},
] 

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vulero_dialer.utils.jinja_methods",
# 	"filters": "vulero_dialer.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vulero_dialer.install.before_install"
# after_install = "vulero_dialer.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vulero_dialer.uninstall.before_uninstall"
# after_uninstall = "vulero_dialer.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vulero_dialer.utils.before_app_install"
# after_app_install = "vulero_dialer.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vulero_dialer.utils.before_app_uninstall"
# after_app_uninstall = "vulero_dialer.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vulero_dialer.notifications.get_notification_config"

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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "Call Log" : {
        "after_insert" : [
            "vulero_dialer.config.call_log.create_followup_for_missed_call", 
		]
	},
    "Followup" : {
        "before_save": [
            "vulero_dialer.config.call_log.update_call_log_on_followup_change"
		]
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "cron": {
	# 	 "* * * * *": [
	# 		"vulero_dialer.tasks.run_call_logs"
	# 	]
	# }
	# 	"vulero_dialer.tasks.all"
	# ],
	# "daily": [
	# 	"vulero_dialer.tasks.daily"
	# ],
	"hourly": [
		"vulero_dialer.config.call_log.fetch_and_process_all_call_logs"
	],
	# "weekly": [
	# 	"vulero_dialer.tasks.weekly"
	# ],
	# "monthly": [
	# 	"vulero_dialer.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "vulero_dialer.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vulero_dialer.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vulero_dialer.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vulero_dialer.utils.before_request"]
# after_request = ["vulero_dialer.utils.after_request"]

# Job Events
# ----------
# before_job = ["vulero_dialer.utils.before_job"]
# after_job = ["vulero_dialer.utils.after_job"]

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
# 	"vulero_dialer.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

