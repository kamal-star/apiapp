app_name = "apiapp"
app_title = "API APP"
app_publisher = "kamal"
app_description = "api"
app_email = "kamal.maharofficial@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/apiapp/css/apiapp.css"
# app_include_js = "/assets/apiapp/js/apiapp.js"

# include js, css files in header of web template
# web_include_css = "/assets/apiapp/css/apiapp.css"
# web_include_js = "/assets/apiapp/js/apiapp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "apiapp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "apiapp/public/icons.svg"

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
# 	"methods": "apiapp.utils.jinja_methods",
# 	"filters": "apiapp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "apiapp.install.before_install"
# after_install = "apiapp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "apiapp.uninstall.before_uninstall"
# after_uninstall = "apiapp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "apiapp.utils.before_app_install"
# after_app_install = "apiapp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "apiapp.utils.before_app_uninstall"
# after_app_uninstall = "apiapp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "apiapp.notifications.get_notification_config"

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
        "Customer": {
        "after_insert": "apiapp.custom_methods.post_customer_to_external_api",
        "on_update": "apiapp.custom_methods.update_customer_status_and_fetch_data"
        },
        "Hub": {
        "after_insert": "apiapp.custom_methods.post_hub_to_external_api",
        "on_update": "apiapp.custom_methods.update_hub_status_and_fetch_data"
        },
	"Post Office": {
        "after_insert": "apiapp.custom_methods.post_postoffice_to_external_api",
        "on_update": "apiapp.custom_methods.update_postoffice_status_and_fetch_data"
        },
	"Driver": {
        "after_insert": "apiapp.custom_methods.post_driver_to_external_api",
        "on_update": "apiapp.custom_methods.update_driver_status_and_fetch_data"
        },
	"Service Request": {
        "after_insert": "apiapp.custom_methods.post_service_request_to_external_api",
        "on_update": "apiapp.custom_methods.update_service_request_status_and_fetch_data"
        },
        "Vehicle": {
        "after_insert": "apiapp.custom_methods.post_vehicle_to_external_api",
        "on_update": "apiapp.custom_methods.update_vehicle_status_and_fetch_data"
        },
        "Vehicle Assignment": {
        "after_insert": "apiapp.custom_methods.post_vehiclea_to_external_api",
        "on_update": "apiapp.custom_methods.update_vehiclea_status_and_fetch_data"
        }
        # "Shipment Delivery": {
        # "before_save": "apiapp.custom_methods.send_data_to_optimize_routechild1"
        # # "on_update": "apiapp.esri.send_data_to_optimize_route"
        # }
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"apiapp.tasks.all"
# 	],
# 	"daily": [
# 		"apiapp.tasks.daily"
# 	],
# 	"hourly": [
# 		"apiapp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"apiapp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"apiapp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "apiapp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "apiapp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "apiapp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["apiapp.utils.before_request"]
# after_request = ["apiapp.utils.after_request"]

# Job Events
# ----------
# before_job = ["apiapp.utils.before_job"]
# after_job = ["apiapp.utils.after_job"]

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
# 	"apiapp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

