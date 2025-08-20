import frappe
import frappe.auth
import json
from frappe.utils import now
from frappe import _  # ✅ REQUIRED for frappe.throw to work

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

    frappe.local.response["sid"] = frappe.session.sid

    frappe.local.response["message"] = {
        "success_key": 1,
        "message": "Login successful",
        "timestamp": now(),
        "data": {
            "api_key": user.api_key,
            "api_secret": api_secret,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "roles": [r.role for r in user.get("roles")],
            "last_login": user.last_login,
            "mobile_no": user.mobile_no,
            "phone": user.phone,
            "language": user.language
        }
    }

def compose_api_key(user):
    user_doc = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=23)

    if not user_doc.api_key:
        user_doc.api_key = frappe.generate_hash(length=23)

    user_doc.api_secret = api_secret
    user_doc.save(ignore_permissions=True)
    return api_secret


@frappe.whitelist( allow_guest=True)
def get_user_info():
    try:
        
        user = frappe.session.user
        

        if not user or user == "Guest":
            frappe.throw(_("Invalid or expired session. Please login again."), frappe.AuthenticationError)

        user_doc = frappe.get_doc("User", user)
        print("The user doc is", user_doc)
        
        

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
                "language": user_doc.language,
                "profile_img": user_doc.user_image  # ✅ Include image URL here
                
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

@frappe.whitelist(allow_guest=False)
def update_user_info(first_name=None, middle_name=None, last_name=None, mobile_no=None):
    user = frappe.session.user
    if user == "Guest":
        frappe.throw("Login required")

    doc = frappe.get_doc("User", user)
    if first_name: doc.first_name = first_name
    if middle_name is not None: doc.middle_name = middle_name  # can be blank
    if last_name is not None: doc.last_name = last_name
    if mobile_no: doc.mobile_no = mobile_no

    doc.save(ignore_permissions=True)

    return {"success": True, "message": "Updated successfully"}
