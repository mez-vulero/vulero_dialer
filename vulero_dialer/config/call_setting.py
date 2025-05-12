import frappe
from frappe import _
import requests 

@frappe.whitelist(allow_guest=False)
def get_user_settings():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in to access this method"), frappe.PermissionError)

    try:
        settings = frappe.get_all('Extensions', filters={'user_link': user}, fields=['organization_id', 'user_link', 'extension'])
        if settings:
            settings = settings[0]
            response = make_outgoing_call(settings['organization_id'], settings['extension'])
            return response
        else:
            return None
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'get_user_settings API failed')
        return None 


@frappe.whitelist(allow_guest=False)
def get_queue_settings():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in to access this method"), frappe.PermissionError)

    try:
        settings = frappe.get_all('Extensions', filters={'user_link': user}, fields=['join_dtmf', 'leave_dtmf', 'extension'])
        if settings:
            settings = settings[0]
            return settings
        else:
            return []
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'get_queue_settings API failed')
        return None 


def make_outgoing_call(organization_id, extension):
    settings = frappe.get_doc('Global Settings')
    url = f"https://etw-pbx-cloud1.websprix.com/api/v2/onboard//get_ip_info/{organization_id}/{extension}/1"
    headers = {
        'x-api-key': settings.api_key, 
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {'error': 'Failed to make outgoing call', 'status_code': response.status_code}
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), 'Outgoing call failed')
        return None

