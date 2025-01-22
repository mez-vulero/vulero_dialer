// vulero_dialer/public/js/doctype_scripts.js

$(document).ready(function() {
    function addCallButton(doctype, phoneField, mobileField) {
        frappe.ui.form.on(doctype, {
            refresh(frm) {
                frm.add_custom_button('<i class="fa fa-phone"></i> Call', () => {
                    if (frm.doc[phoneField] && frm.doc[mobileField]) {
                        // If both are set, ask the user which one to call
                        let options = [
                            {label: __('Phone: ') + frm.doc[phoneField], value: frm.doc[phoneField]},
                            {label: __('Mobile: ') + frm.doc[mobileField], value: frm.doc[mobileField]}
                        ];
                        frappe.prompt([
                            {'fieldname': 'number_to_call', 'fieldtype': 'Select', 'label': 'Which number to call?', 'options': options, 'reqd': 1}
                        ], (values) => {
                            triggerCallEvent(values.number_to_call);
                        }, __('Call ' + doctype), __('<i class="fa fa-phone"></i> Call'));
                    } else if (frm.doc[phoneField] || frm.doc[mobileField]) {
                        // If only one is set, call directly
                        let number_to_call = frm.doc[phoneField] || frm.doc[mobileField];
                        triggerCallEvent(number_to_call);            
                    } else {
                        // If neither phone nor mobile_no is set, inform the user
                        frappe.msgprint(__('No contact number found for this ' + doctype.toLowerCase() + '.'));
                    }
                });
            }
        });
    }

    function triggerCallEvent(number) {
        window.dispatchEvent(new CustomEvent('callEvent', {
            detail: { number: number }
        }));
    }

    // Add call button to multiple doctypes
    addCallButton('Lead', 'phone', 'mobile_no');
    addCallButton('Opportunity', 'phone', 'mobile_no');
    addCallButton('Contact', 'phone', 'mobile_no');
    addCallButton('Customer', 'phone', 'mobile_no');
    addCallButton('Student', 'phone', 'mobile_no');
    addCallButton("Tourist", "mobile_no", "");
    addCallButton('Followup', 'phone', 'mobile_no');

});
