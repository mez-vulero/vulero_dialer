import frappe

@frappe.whitelist(allow_guest=False)
def get_contact_info(formattedNumber):
    settings = frappe.get_doc("Global Settings")
    contacts = frappe.get_all(settings.check_contacts_info_from,
                           fields=["name", "phone", "first_name", "middle_name", "last_name", "modified"],
                           or_filters=[("phone", "=", formattedNumber), ("mobile_no", "=", formattedNumber)],
                           order_by='modified desc',
                           limit=1)

    formattedNumberWithCountryCode = '+251' + formattedNumber.lstrip('0')

    open_file = frappe.get_all(settings.open_file,
                            fields=["name"],
                            or_filters=[
                                ("phone", "=", formattedNumber),
                                ("mobile_no", "=", formattedNumber),
                                ("phone", "=", formattedNumberWithCountryCode),
                                ("mobile_no", "=", formattedNumberWithCountryCode)
                            ],
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

    if open_file and open_file[0]:
        open_file = open_file[0]
        open_file_name = open_file.get('name', '').strip();
    else:
        open_file_name = ''
    
    response = {
        'doc_type': settings.check_contacts_info_from.lower(),
        'file_doc_type': settings.open_file.lower(),
        'open_file_name': open_file_name, 
        'data': contact
    }
    return response
