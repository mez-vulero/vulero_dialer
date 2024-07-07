import frappe

@frappe.whitelist(allow_guest=False)
def get_contact_info(formattedNumber):
    settings = frappe.get_doc("Global Settings")
    contacts = frappe.get_all(settings.check_contacts_info_from,
                           fields=["name", "phone", "first_name", "middle_name", "last_name", "modified"],
                           or_filters=[("phone", "=", formattedNumber), ("mobile_no", "=", formattedNumber)],
                           order_by='modified desc',
                           limit=1)

    if contacts and contacts[0]:
        contact = contacts[0]
        first_name = contact.get('first_name', '').strip() if contact.get('first_name') else ''
        middle_name = contact.get('middle_name', '').strip() if contact.get('middle_name') else ''
        last_name = contact.get('last_name', '').strip() if contact.get('last_name') else ''
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        contact['full_name'] = full_name
    else:
        contact = []
    
    response = {
        'doc_type': settings.check_contacts_info_from.lower(),
        'data': contact
    }
    return response

