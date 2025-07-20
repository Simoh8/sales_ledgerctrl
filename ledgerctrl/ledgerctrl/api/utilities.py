import frappe



@frappe.whitelist()
def get_user_delivery_trips(user):
    user = frappe.session.user

    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")

    if not employee:
        return {
            "success_key": 0,
            "message": "No Employee record linked to this user."
        }

    # Fetch Delivery Trips assigned to this employee
    trips = frappe.get_all("Delivery Trip",
        filters={"driver": employee},
        fields=["name", "status", "vehicle", "docstatus"]
    )

    return {
        "success_key": 1,
        "message": "Trips fetched successfully.",
        "employee": employee,
        "delivery_trips": trips
    }


