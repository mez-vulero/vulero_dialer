$(document).ready(function() {
frappe.ui.form.on('Opportunity', {
    refresh(frm) {
        // Adds a custom button with a phone icon to the Lead form
        frm.add_custom_button('<i class="fa fa-phone"></i> Call', () => {
            // Check if both phone and mobile_no are set
            if (frm.doc.phone && frm.doc.mobile_no) {
                // If both are set, ask the user which one to call
                let options = [
                    {label: __('Phone: ') + frm.doc.phone, value: 'phone'},
                    {label: __('Mobile: ') + frm.doc.mobile_no, value: 'mobile'}
                ];

                frappe.prompt([
                    {'fieldname': 'number_to_call', 'fieldtype': 'Select', 'label': 'Which number to call?', 'options': options, 'reqd': 1}
                ],
                (values) => {
                    // Logic to initiate call to the selected number
                    let number_to_call = values.number_to_call === 'phone' ? frm.doc.phone : frm.doc.mobile_no;
                    frappe.msgprint(__('Initiating call to ') + number_to_call);
                    // Integrate call initiation logic here
                },
                __('Call Lead'),
                __('<i class="fa fa-phone"></i> Call')
                );
            } else if (frm.doc.phone || frm.doc.mobile_no) {
                // If only one is set, call directly
                let number_to_call = frm.doc.phone ? frm.doc.phone : frm.doc.mobile_no;
                frappe.msgprint(__('Initiating call to ') + number_to_call);
                // Integrate call initiation logic here
            } else {
                // If neither phone nor mobile_no is set, inform the user
                frappe.msgprint(__('No contact number found for this opportunity.'));
            }
        });
    }
});
});
