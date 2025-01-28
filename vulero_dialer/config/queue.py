import frappe
import requests

@frappe.whitelist()
def add_to_queue():
    """
    Add to queue operation (stub).
    """
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            'Extensions',
            filters={'user_link': user},
            fields=['user_link', 'extension', 'queue_name' ]
        )
        global_settings = frappe.get_doc('Global Settings')
        if settings:
            settings = settings[0]
        else:
            return {"status": "error", "message": "Settings not found for user"}
        # Construct the interface value
        interface = f"{global_settings.organization_id}S{settings['extension']}"
        url = f"https://etw-pbx-cloud1.websprix.com/api/v2/member/{global_settings.organization_id}/add"

        # Prepare request payload and headers
        body = {
            "queue_name": settings['queue_name'],
            "interface": interface
        }
        headers = {
            'x-api-key': global_settings.api_key,
        }

        # Make the API call
        response = requests.post(url, json=body, headers=headers)
        if response.status_code in [200, 201]:
            return {"status": "success", "message": "added"}
        else:
            frappe.log_error(
                f"Failed to add to queue: {response.status_code} - {response.text}",
                "Add to Queue Error"
            )
            return {"status": "error", "message": "Failed to add to queue", "details": response.text}
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Add to Queue Request Exception")
        return {"status": "error", "message": "Failed to add to queue due to request error"}

    except Exception as e:
        frappe.log_error(str(e), "Add to Queue General Exception")
        return {"status": "error", "message": "An unexpected error occurred"}

@frappe.whitelist()
def remove_from_queue():
    """
    Remove from queue operation (stub).
    """
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            'Extensions',
            filters={'user_link': user},
            fields=['user_link', 'extension', 'queue_name' ]
        )
        global_settings = frappe.get_doc('Global Settings')
        if settings:
            settings = settings[0]
        else:
            return {"status": "error", "message": "Settings not found for user"}
        # Construct the interface value
        interface = f"{global_settings.organization_id}S{settings['extension']}"
        url = f"https://etw-pbx-cloud1.websprix.com/api/v2/member/{global_settings.organization_id}/remove"

        # Prepare request payload and headers
        body = {
            "queue_name": settings['queue_name'],
            "interface": interface
        }
        headers = {
            'x-api-key': global_settings.api_key,
        }

        # Make the API call
        response = requests.delete(url, json=body, headers=headers)
        if response.status_code in [200, 201]:
            return {"status": "success", "message": "removed"}
        else:
            frappe.log_error(
                f"Failed to add to queue: {response.status_code} - {response.text}",
                "Add to Queue Error"
            )
            return {"status": "error", "message": "Failed to add to queue", "details": response.text}
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Add to Queue Request Exception")
        return {"status": "error", "message": "Failed to add to queue due to request error"}

    except Exception as e:
        frappe.log_error(str(e), "Add to Queue General Exception")
        return {"status": "error", "message": "An unexpected error occurred"}

@frappe.whitelist()
def get_queue_status():
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            'Extensions',
            filters={'user_link': user},
            fields=['user_link', 'extension', 'queue_name']
        )
        global_settings = frappe.get_doc('Global Settings')
        if settings:
            settings = settings[0]
        else:
            return {"status": "error", "message": "Settings not found for user"}

        interface = f"{global_settings.organization_id}S{settings['extension']}"
        url = f"https://etw-pbx-cloud1.websprix.com/api/v2/member/{global_settings.organization_id}/queues_for_agent?interface={interface}"

        # Prepare headers for the request
        headers = {
            'x-api-key': global_settings.api_key,
        }

        # Make the API call
        response = requests.get(url, headers=headers)
        if response.status_code in [200, 201]:
            # Try to parse the JSON response
            try:
                queues = response.json()
            except ValueError as e:
                return {"status": "error", "message": f"Failed to parse JSON response: {str(e)}"}

            # Check if the response is a list and contains the queue we're interested in
            for queue in queues['result']:
                if queue['full_queue_name'] == settings['queue_name']:
                    return {"status": "success", "is_member": queue['is_member']}
            return {"status": "error", "message": "Queue not found for the agent"}
        else:
            frappe.log_error(
                f"Failed to fetch queues: {response.status_code} - {response.text}",
                "Get Queue Status Error"
            )
            return {"status": "error", "message": "Failed to fetch queue status", "details": response.text}
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Queue Status Request Exception")
        return {"status": "error", "message": "Failed to fetch queue status due to request error"}

    except Exception as e:
        frappe.log_error(str(e), "Queue Status General Exception")
        return {"status": "error", "message": "An unexpected error occurred"}

