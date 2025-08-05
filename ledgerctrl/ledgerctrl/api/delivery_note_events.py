import frappe
import random
from frappe import _
from frappe.exceptions import ValidationError


def generate_otp(doc, method):
    """
    Generate and assign a 6-digit OTP to the Delivery Note upon first submission.
    This OTP is stored in custom_otp_code.
    """
    if doc.custom_otp_code:
        return  # OTP already exists; don't regenerate

    otp = _create_otp()
    doc.custom_otp_code = otp

    # OPTIONAL: send OTP via email/SMS (implement based on your needs)
    # _send_otp(doc.customer, otp)

    frappe.msgprint(_("OTP generated for Delivery Note: {0}").format(otp))


def validate_otp(doc, method):
    """
    Ensure the user provides a correct OTP when setting the Delivery Note status to 'Closed'.
    """
    if doc.docstatus != 1:
        return  # Only validate OTP for submitted documents

    if doc.status != "Closed":
        return  # Only apply OTP check when closing

    _ensure_otp_fields_present(doc)
    _validate_otp_match(doc)

    doc.custom_otp_verified = 1


# --- Helpers --- #

def _create_otp(length=6):
    return str(random.randint(10**(length - 1), (10**length) - 1))


def _ensure_otp_fields_present(doc):
    if not doc.custom_otp_code:
        raise ValidationError(_("No OTP has been generated for this Delivery Note."))

    if not doc.custom_user_otp:
        raise ValidationError(_("Please enter the OTP to close this Delivery Note."))


def _validate_otp_match(doc):
    if doc.custom_user_otp != doc.custom_otp_code:
        raise ValidationError(_("Invalid OTP. Cannot close this Delivery Note."))


# Optional (stub): sending OTP via email or SMS
def _send_otp(customer_name, otp):
    """Stub for integrating OTP delivery via SMS or email."""
    # Example: frappe.sendmail(...)
    # Or integrate Twilio/other providers
    pass



class DeliveryNoteCloser:
    def __init__(self, name: str, otp: str):
        self.name = name
        self.otp = otp
        self.doc = self._get_doc()

    def _get_doc(self):
        try:
            return frappe.get_doc("Delivery Note", self.name)
        except frappe.DoesNotExistError:
            raise ValidationError(_("Delivery Note not found"))

    def validate_status(self):
        if self.doc.docstatus != 1:
            raise ValidationError(_("Only submitted Delivery Notes can be closed"))

        if self.doc.status == "Closed":
            raise ValidationError(_("Delivery Note is already closed"))

    def validate_otp(self):
        stored_otp = self.doc.custom_otp_code
        if not stored_otp:
            raise ValidationError(_("OTP is not generated for this Delivery Note"))

        if self.otp != stored_otp:
            raise ValidationError(_("Incorrect OTP"))

    def close(self):
        self.doc.custom_user_otp = self.otp
        self.doc.custom_otp_verified = 1
        self.doc.status = "Closed"
        self.doc.save()

    def execute(self):
        self.validate_status()
        self.validate_otp()
        self.close()
        return {
            "message": _("Delivery Note closed successfully"),
            "delivery_note": self.doc.name,
            "status": self.doc.status
        }


@frappe.whitelist()
def close_delivery_note_with_otp(delivery_note_name: str, otp_input: str):
    """API endpoint to close a Delivery Note using OTP (used by driver apps)."""
    if not delivery_note_name or not otp_input:
        raise ValidationError(_("Both delivery note and OTP are required"))

    return DeliveryNoteCloser(delivery_note_name, otp_input).execute()
