from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist()
def get_dashboard_stats():
    try:
        # Get outstanding invoices sum
        outstanding_invoices = frappe.db.sql("""
            SELECT SUM(outstanding_amount) 
            FROM `tabSales Invoice`
            WHERE docstatus = 1 AND outstanding_amount > 0
        """)[0][0] or 0

        # Get overdue invoices sum
        overdue_invoices = frappe.db.sql("""
            SELECT SUM(outstanding_amount) 
            FROM `tabSales Invoice`
            WHERE docstatus = 1 AND outstanding_amount > 0 AND due_date < %s
        """, (datetime.now().date()), as_dict=0)[0][0] or 0

        # Get recent payments sum (last 30 days)
        recent_payments = frappe.db.sql("""
            SELECT SUM(paid_amount) 
            FROM `tabPayment Entry`
            WHERE docstatus = 1 AND posting_date >= %s
        """, (datetime.now() - timedelta(days=30)).date(), as_dict=0)[0][0] or 0

        # Get open tickets count
        open_tickets = frappe.db.count("Issue", filters={"status": "Open"})

        return {
            "success_key": 1,
            "outstanding_invoices": outstanding_invoices,
            "overdue_invoices": overdue_invoices,
            "recent_payments": recent_payments,
            "open_tickets": open_tickets
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch dashboard stats")
        return {
            "success_key": 0,
            "message": str(e)
        }

@frappe.whitelist()
def get_recent_activity():
    try:
        activity = []
        
        # Get recent payments (last 5)
        payments = frappe.db.sql("""
            SELECT name as id, 'payment' as type, paid_amount as amount, 
                   posting_date as date, 'completed' as status,
                   (SELECT reference_name FROM `tabPayment Entry Reference` 
                    WHERE parent=pe.name AND reference_doctype='Sales Invoice' LIMIT 1) as reference
            FROM `tabPayment Entry` pe
            WHERE docstatus = 1
            ORDER BY posting_date DESC
            LIMIT 5
        """, as_dict=1)
        activity.extend(payments)
        
        # Get recent invoices (last 5)
        invoices = frappe.db.sql("""
            SELECT name as id, 'invoice' as type, grand_total as amount, 
                   posting_date as date, 
                   CASE WHEN outstanding_amount > 0 THEN 'pending' ELSE 'paid' END as status,
                   name as reference
            FROM `tabSales Invoice`
            WHERE docstatus = 1
            ORDER BY posting_date DESC
            LIMIT 5
        """, as_dict=1)
        activity.extend(invoices)
        
        # Get recent tickets (last 5)
        tickets = frappe.db.sql("""
            SELECT name as id, 'ticket' as type, subject, 
                   creation as date, status
            FROM `tabIssue`
            ORDER BY creation DESC
            LIMIT 5
        """, as_dict=1)
        activity.extend(tickets)
        
        # Sort all activity by date
        activity.sort(key=lambda x: x.date, reverse=True)
        
        return {
            "success_key": 1,
            "activity": activity[:10]  # Return top 10 most recent
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch recent activity")
        return {
            "success_key": 0,
            "message": str(e)
        }