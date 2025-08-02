import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_assigned_orders():
    user = frappe.session.user

    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not employee:
        return {
            "success_key": 0,
            "error": "No Employee found for the current user."
        }

    trips = frappe.get_all(
        "Delivery Trip",
        filters={"employee": employee, "status": ["!=", "Cancelled"]},
        fields=["name", "driver_name", "total_distance", "departure_time", "status"],
        order_by="modified desc",
        limit_page_length=50
    )

    trip_data = []

    for trip in trips:
        stops = frappe.get_all(
            "Delivery Stop",
            filters={"parent": trip.name},
            fields=[
                "name", "customer", "customer_address", "customer_contact",
                "grand_total", "distance", "lat", "lng", "delivery_note"
            ]
        )

        items = []
        for stop in stops:
            # Get item list from delivery note (if exists)
            note_items = []
            if stop.delivery_note:
                note_items = frappe.get_all(
                    "Delivery Note Item",
                    filters={"parent": stop.delivery_note},
                    fields=["item_name", "qty", "rate"]
                )

            items.append({
                "id": stop.name,
                "name": stop.customer,
                "description": stop.customer_address or "",
                "quantity": 1,
                "price": float(stop.grand_total or 0),
                "latitude": float(stop.lat or 0),
                "longitude": float(stop.lng or 0),
                "delivery_note": stop.delivery_note,
                "note_items": note_items
            })

        trip_data.append({
            "id": trip.name,
            "customer_name": trip.driver_name,
            "customer_phone": "",
            "delivery_address": f"{len(stops)} stops",
            "distance": float(trip.total_distance or 0),
            "amount": sum(item["price"] for item in items),
            "item_count": len(items),
            "order_time": trip.departure_time.strftime("%Y-%m-%d %H:%M:%S") if trip.departure_time else "",
            "status": trip.status,
            "items": items
        })

    return {
        "success_key": 1,
        "data": trip_data
    }
