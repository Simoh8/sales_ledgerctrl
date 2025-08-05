frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status !== 'Closed') {
            frm.add_custom_button(__('Close with OTP'), function () {
                frappe.prompt({
                    label: 'Enter OTP',
                    fieldname: 'otp_input',
                    fieldtype: 'Data',
                    reqd: 1
                }, function (values) {
                    frm.set_value('custom_user_otp', values.otp_input); // use custom field
                    frm.set_value('status', 'Closed');
                    frm.save();
                }, __('OTP Required'));
            });
        }
    }
});
