import frappe

@frappe.whitelist(allow_guest=False)
def get_contact_info(formattedNumber):
    settings = frappe.get_doc("Global Settings")
    contacts = frappe.get_all(settings.check_contacts_info_from,
                           fields=["name", "phone", "first_name", "modified"],
                           or_filters=[("phone", "=", formattedNumber), ("mobile_no", "=", formattedNumber)],
                           order_by='modified desc',
                           limit=1)
    if contacts:
        contact = contacts[0]
    else:
        contact = []
    
    response = {
        'doc_type': settings.check_contacts_info_from.lower(),
        'data': contact
    }
    return response

