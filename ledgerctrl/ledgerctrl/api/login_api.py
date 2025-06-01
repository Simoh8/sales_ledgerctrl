import fractions
import frappe
import frappe.auth

@frappe.whitelist(allow_guest=True)

def user_logn(usr, passwd):
    
    try:
        login_mngr =frappe.auth.LoginManager()
        login_mngr =
        
    