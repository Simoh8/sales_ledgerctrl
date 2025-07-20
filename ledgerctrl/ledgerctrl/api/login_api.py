import frappe
import frappe.auth
from frappe.utils import now

@frappe.whitelist(allow_guest=True)
def user_logn(usr, passwd):
    try:
        login_mngr = frappe.auth.LoginManager()
        login_mngr.authenticate(user=usr, pwd=passwd)
        login_mngr.post_login()
    except frappe.exceptions.AuthenticationError as e:
        frappe.clear_messages()

        frappe.local.response["message"] = {
            "success_key": 0,
            "message": "Invalid login details. Please try again.",
            "timestamp": now()
        }
        return

    user = frappe.get_doc('User', frappe.session.user)
    api_secret = compose_api_key(frappe.session.user)

    frappe.local.response["message"] = {
        "success_key": 1,
        "message": "Login successful",
        "timestamp": now(),
        "data": {
            "sid": frappe.session.sid,
            "api_key": user.api_key,
            "api_secret": api_secret,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "roles": [r.role for r in user.get("roles")],
            "last_login": user.last_login,
        }
    }

    
def compose_api_key(user):
    user_doc = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=23)

    if not user_doc.api_key:
        user_doc.api_key = frappe.generate_hash(length=23)

    user_doc.api_secret = api_secret
    user_doc.save(ignore_permissions=True)  # allow saving if called from guest context

    return api_secret



@frappe.whitelist()
def get_user_info():
    """
    Fetch user details using active login session (sid).
    This works only if the client includes 'sid' cookie in requests.
    """

    try:
        user = frappe.session.user

        if not user or user == "Guest":
            frappe.throw(_("Invalid or expired session. Please login again."), frappe.AuthenticationError)

        user_doc = frappe.get_doc("User", user)

        return {
            "success_key": 1,
            "message": "User info fetched successfully.",
            "data": {
                "full_name": user_doc.full_name,
                "username": user_doc.username,
                "email": user_doc.email,
                "mobile_no": user_doc.mobile_no,
                "phone": user_doc.phone,
                "roles": [r.role for r in user_doc.roles],
                "enabled": user_doc.enabled,
                "last_login": user_doc.last_login,
                "language": user_doc.language
            }
        }

    except frappe.AuthenticationError as ae:
        frappe.local.response.http_status_code = 401
        return {
            "success_key": 0,
            "message": f"Authentication failed: {str(ae)}"
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "GetUserInfo Error")
        frappe.local.response.http_status_code = 500
        return {
            "success_key": 0,
            "message": f"Error: {str(e)}"
        }
