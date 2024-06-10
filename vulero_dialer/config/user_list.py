import frappe
from frappe import _
import requests 

@frappe.whitelist(allow_guest=False)
def fetch_users_to_transfer():
    settings = frappe.get_doc('Global Settings')
    url = f"https://etw-pbx-cloud1.websprix.com/api/v1/cust_ext/{settings.organization_id}/cust"
    headers = {'x-api-key': settings.api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            frappe.log_error(f"Failed to fetch users. Status code: {response.status_code}", 'Fetch Users Error')
            return {'error': 'Failed to fetch users', 'status_code': response.status_code}
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), 'Fetch Users API Error')
        return {'error': 'API request failed', 'exception': str(e)}

