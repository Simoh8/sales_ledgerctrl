app_name = "ledgerctrl"
app_title = "ledgerctrl"
app_publisher = "simon muturi "
app_description = "an app that has mobile app apis for the user to login like a driver and also a sales people"
app_email = "simomutu8@gmail.com"
app_license = "mit"

# Apps
# ------------------
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ledgerctrl",
# 		"logo": "/assets/ledgerctrl/logo.png",
# 		"title": "ledgerctrl",
# 		"route": "/ledgerctrl",
# 		"has_permission": "ledgerctrl.api.permission.has_app_permission"
# 	}
# ]rnnUCClWCP0U2wHL8trUOuJrgkMuJwMukdoCLbwC

# Includes in <head>
# ------------------
app_include_js = [
    "https://unpkg.com/leaflet@1.9.3/dist/leaflet.js",
    "https://maps.googleapis.com/maps/api/js?key=AIzaSyClcVmsDzi8fZ_pXoIzBqZHhXj7_Yvund0&libraries=places",
    "/assets/ledgerctrl/js/address_map.js",
    "/assets/ledgerctrl/js/delivery_note.js",
        ]


# doctype_js = {
#     "Address": "ledgerctrl/js/address_map.js"
# }

app_include_css = [
    "https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
]

# include js, css files in header of desk.html
# app_include_css = "/assets/ledgerctrl/css/ledgerctrl.css"
# app_include_js = "/assets/ledgerctrl/js/ledgerctrl.js"

# include js, css files in header of web template
# web_include_css = "/assets/ledgerctrl/css/ledgerctrl.css"
# web_include_js = "/assets/ledgerctrl/js/ledgerctrl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ledgerctrl/public/scss/website"

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
# app_include_icons = "ledgerctrl/public/icons.svg"

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
# 	"methods": "ledgerctrl.utils.jinja_methods",
# 	"filters": "ledgerctrl.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ledgerctrl.install.before_install"
# after_install = "ledgerctrl.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ledgerctrl.uninstall.before_uninstall"
# after_uninstall = "ledgerctrl.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ledgerctrl.utils.before_app_install"
# after_app_install = "ledgerctrl.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ledgerctrl.utils.before_app_uninstall"
# after_app_uninstall = "ledgerctrl.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ledgerctrl.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "Delivery Note": {
        "before_submit": "ledgerctrl.ledgerctrl.api.delivery_note_events.generate_otp",
        "before_save": "ledgerctrl.ledgerctrl.api.delivery_note_events.validate_otp"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ledgerctrl.tasks.all"
# 	],
# 	"daily": [
# 		"ledgerctrl.tasks.daily"
# 	],
# 	"hourly": [
# 		"ledgerctrl.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ledgerctrl.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ledgerctrl.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ledgerctrl.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ledgerctrl.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ledgerctrl.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ledgerctrl.utils.before_request"]
# after_request = ["ledgerctrl.utils.after_request"]

# Job Events
# ----------
# before_job = ["ledgerctrl.utils.before_job"]
# after_job = ["ledgerctrl.utils.after_job"]

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
# 	"ledgerctrl.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

