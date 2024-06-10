$(document).ready(function() {
frappe.ui.form.on('Lead', {
    refresh(frm) {
        
        frm.add_custom_button('<i class="fa fa-phone"></i> Call', () => {
            
            if (frm.doc.phone && frm.doc.mobile_no) {
                // If both are set, ask the user which one to call
                let options = [
                    {label: __('Phone: ') + frm.doc.phone, value: frm.doc.phone},
                    {label: __('Mobile: ') + frm.doc.mobile_no, value: frm.doc.mobile_no}
                ];

                frappe.prompt([
                    {'fieldname': 'number_to_call', 'fieldtype': 'Select', 'label': 'Which number to call?', 'options': options, 'reqd': 1}
                ],
                (values) => {
                    // Trigger the call event with the selected number
                    triggerCallEvent(values.number_to_call);
                },
                __('Call Lead'),
                __('<i class="fa fa-phone"></i> Call')
                );
            } else if (frm.doc.phone || frm.doc.mobile_no) {
                // If only one is set, call directly
                let number_to_call = frm.doc.phone || frm.doc.mobile_no;
                triggerCallEvent(number_to_call);            
            } else {
                // If neither phone nor mobile_no is set, inform the user
                frappe.msgprint(__('No contact number found for this lead.'));
            }
        });
    }
});

function triggerCallEvent(number) {
    window.dispatchEvent(new CustomEvent('callEvent', {
        detail: { number: number }
    }));
   }
});
