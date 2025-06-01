import frappe
import frappe.auth

@frappe.whitelist(allow_guest=True)
def user_logn(usr, passwd):
    
    try:
        login_mngr =frappe.auth.LoginManager()
        login_mngr.authenticate(user=usr, pwd=passwd)
        login_mngr.post_login()
        
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] ={
            "success_key" :0,
            "message": "Authentication Error"
        }
        
        return
    
    api_prod =compose_api_key(frappe.session.user)
    user=frappe.get_doc('User', frappe.session.user)
    
    frappe.local.response["message"] ={
            "success_key" :1,
            "message": "Authentication Success",
            "sid":frappe.session.sid,
            "api_key":user.api_key,
            "api_secret": api_prod,
            "username":user.username,
            "mail":user.email
        }
    
def compose_api_key(user):
    user_infor= frappe.get_doc('User', user)
    api_secrt= frappe.generate_hash(length=23)
    
    
    if not user_infor.api_key:
        api_key= frappe.generate_hash(length=23)
        user_infor.api_key=api_key
        
    user_infor.api_secret=api_secrt
    user_infor.save()
    
    
    return api_secrt
        
    

    