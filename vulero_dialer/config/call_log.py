import frappe
import requests
import datetime
import uuid
import hashlib
from globedock.utils.assignment import make_assignment, make_followup, make_todo
from globedock.utils.date import get_due_date



@frappe.whitelist(allow_guest=False)
def fetch_and_process_all_call_logs():
    """
    Fetch incoming call logs from the external API and process them into the Call Log doctype.
    """
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            "Extensions",
            fields=["user_link", "extension", "queue_name"]
        )
        
        if not settings:
            return {"status": "error", "message": "Settings not found for the current user"}
        
        for setting in settings:
            user_link = setting.user_link  # employee_user_id
            extension = setting.extension

            # Fetch global settings for the API key
            global_settings = frappe.get_doc('Global Settings')

            # Construct the URL using the fetched extension
            url = f"https://etw-pbx-cloud1.websprix.com/api/v2/cust_ext/{global_settings.organization_id}/call_logs/{extension}?dir=in"

            # Prepare request headers
            headers = {
                'x-api-key': global_settings.api_key,
            }

            # Make the API call
            response = requests.get(url, headers=headers)
            if response.status_code not in [200, 201]:
                frappe.log_error(
                    f"Failed to fetch Incoming Calls {response.status_code} - {response.text}",
                    "Incoming Call Fetching Error"
                )
                return {"status": "error", "message": "Failed to fetch calls", "details": response.text}
            
            call_logs = response.json()  # Assuming the response is a JSON list
            for log in call_logs['result']:
                process_incoming_call_log (log=log, user_link=user_link)

            frappe.db.commit()  # Commit changes to the database
            return {"status": "success", "message": "Call logs processed successfully"}
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - Request Exception")
        return {"status": "error", "message": "API request failed", "details": str(e)}
    except Exception as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}

@frappe.whitelist(allow_guest=False)
def fetch_and_process_call_logs():
    """
    Fetch incoming call logs from the external API and process them into the Call Log doctype.
    """
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            "Extensions",
            filters={"user_link": user},
            fields=["user_link", "extension", "queue_name"]
        )
        
        if not settings:
            return {"status": "error", "message": "Settings not found for the current user"}
        
        settings = settings[0]
        user_link = settings.user_link  # employee_user_id
        extension = settings.extension

        # Fetch global settings for the API key
        global_settings = frappe.get_doc('Global Settings')

        # Construct the URL using the fetched extension
        url = f"https://etw-pbx-cloud1.websprix.com/api/v2/cust_ext/{global_settings.organization_id}/call_logs/{extension}?dir=in"

        # Prepare request headers
        headers = {
            'x-api-key': global_settings.api_key,
        }

        # Make the API call
        response = requests.get(url, headers=headers)
        if response.status_code not in [200, 201]:
            frappe.log_error(
                f"Failed to fetch Incoming Calls {response.status_code} - {response.text}",
                "Incoming Call Fetching Error"
            )
            return {"status": "error", "message": "Failed to fetch calls", "details": response.text}
        
        call_logs = response.json()  # Assuming the response is a JSON list
        for log in call_logs['result']:        
            process_incoming_call_log (log=log, user_link=user_link)
                
        frappe.db.commit()  # Commit changes to the database
        return {"status": "success", "message": "Call logs processed successfully"}
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - Request Exception")
        return {"status": "error", "message": "API request failed", "details": str(e)}
    except Exception as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}

@frappe.whitelist(allow_guest=False)
def fetch_and_process_offhour_logs():
    """
    Fetch offhour call logs from the external API and process them into the Call Log doctype.
    """
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            "Extensions",
            filters={"user_link": user},
            fields=["user_link", "extension", "queue_name"]
        )
        
        if not settings:
            return {"status": "error", "message": "Settings not found for the current user"}
        
        settings = settings[0]
        user_link = settings.user_link  # employee_user_id
        extension = settings.extension
        queue_name = settings.queue_name

        # Fetch global settings for the API key
        global_settings = frappe.get_doc('Global Settings')

        # Construct the URL using the fetched extension
        url = f"https://etw-pbx-cloud1.websprix.com/api/v2/new-report/{global_settings.organization_id}/{queue_name}/off-hour-callers?page=1&per_page=100"

        # Prepare request headers
        headers = {
            'x-api-key': global_settings.api_key,
        }

        # Make the API call
        response = requests.get(url, headers=headers)
        if response.status_code not in [200, 201]:
            frappe.log_error(
                f"Failed to fetch Offhour Calls {response.status_code} - {response.text}",
                "Incoming Call Fetching Error"
            )
            return {"status": "error", "message": "Failed to fetch calls", "details": response.text}
        
        call_logs = response.json()  # Assuming the response is a JSON list
        for log in call_logs['result']:
            # Check if call log already exists
            existing_log = frappe.get_all(
                "Call Log",
                filters={
                    "start_time": log['created_at'],
                    "from": log["phone"]
                },
                fields=["id"]
            )
            if not existing_log:
                #  unique_id = str(uuid.uuid4())
                #  short_id = hashlib.sha256(unique_id.encode()).hexdigest()[:10]
                #  new_call_log = {
                #      "doctype": "Call Log",
                #      "id": short_id,
                #      "type": "OffHour",
                #      "from": log["phone"],
                #      "queue_name": log["queue_name"],
                #      "status": 'Missed Call',
                #      "start_time": log["created_at"]
                #  }
                # # Insert the new call log
                #  frappe.get_doc(new_call_log).insert(ignore_permissions=True)
                process_incoming_call_log (log=log, user_link=None, off_hour=True)

        frappe.db.commit()  # Commit changes to the database
        return {"status": "success", "message": "Call logs processed successfully"}
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - Request Exception")
        return {"status": "error", "message": "API request failed", "details": str(e)}
    except Exception as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}

@frappe.whitelist(allow_guest=False)
def fetch_and_process_outgoing_call_logs():
    """
    Fetch outgoing call logs from the external API and process them into the Call Log doctype.
    """
    try:
        # Fetch settings for the current user
        user = frappe.session.user
        settings = frappe.get_all(
            "Extensions",
            filters={"user_link": user},
            fields=["user_link", "extension", "queue_name"]
        )
        
        if not settings:
            return {"status": "error", "message": "Settings not found for the current user"}
        
        settings = settings[0]
        user_link = settings.user_link  # employee_user_id
        extension = settings.extension

        # Fetch global settings for the API key
        global_settings = frappe.get_doc('Global Settings')

        # Construct the URL using the fetched extension
        url = f"https://etw-pbx-cloud1.websprix.com/api/v2/cust_ext/{global_settings.organization_id}/call_logs/{extension}?dir=out"

        # Prepare request headers
        headers = {
            'x-api-key': global_settings.api_key,
        }

        # Make the API call
        response = requests.get(url, headers=headers)
        if response.status_code not in [200, 201]:
            frappe.log_error(
                f"Failed to fetch Outgoing Calls {response.status_code} - {response.text}",
                "Outgoing Call Fetching Error"
            )
            return {"status": "error", "message": "Failed to fetch calls", "details": response.text}
        
        call_logs = response.json()  # Assuming the response is a JSON list
        for log in call_logs['result']:
            call_id = log["id"]
            
            # Check if call log already exists
            existing_log = frappe.get_all(
                "Call Log",
                filters={"id": call_id},
                fields=["id"]
            )
            
            if not existing_log:
                # Prepare data for insertion
                new_call_log = {
                    "doctype": "Call Log",
                    "type": "Outgoing",
                    "id": call_id,
                    "from": log["src"],
                    "to": format_phone_number(log["dst"]),
                    "employee_user_id": user_link,  # Set call_received_by to user_link (employee_user_id)
                    "duration": log["duration"],
                    "status": log["disposition"],
                    "recording_url": log["recording_url"],
                    "start_time": log["created_at"]
                }
                
                # Insert the new call log
                frappe.get_doc(new_call_log).insert(ignore_permissions=True)

        frappe.db.commit()  # Commit changes to the database
        return {"status": "success", "message": "Call logs processed successfully"}
    
    except requests.exceptions.RequestException as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - Request Exception")
        return {"status": "error", "message": "API request failed", "details": str(e)}
    except Exception as e:
        frappe.log_error(str(e), "Fetch and Process Call Logs - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}


def process_incoming_call_log (log, user_link=None, off_hour=False):
    try:
        # 2025-01-05 14:09:32.365421
        format = "%Y-%m-%d %H:%M:%S.%f"
        created_at = datetime.datetime.strptime (log["created_at"], format)
        now = datetime.datetime.now ()
        if (created_at > now + datetime.timedelta(days=-2)):
            if (not off_hour): 
                if (log["disposition"] == "NO ANSWER"):
                    existing_log = frappe.get_all(
                            "Call Log",
                            filters={
                                "type": "Incoming",
                                "from": format_phone_number(log["src"]),
                                "status": "NO ANSWER",
                                # "followup_status": ["in", ["Pending", "Failed to Reach"]],
                                "start_time": [">", now + datetime.timedelta(days=-2)]
                            },
                            fields=["name", "start_time", "followup_status"],
                            order_by="start_time desc"
                        )
                    if (existing_log):
                        if (existing_log[0].start_time < created_at):
                            if (existing_log[0].followup_status in ["Pending", "Failed to Reach"]):
                                call_log = frappe.get_doc ("Call Log", existing_log[0].get ("name"))
                                call_log.start_time = log["created_at"]
                                call_log.recording_url = log["recording_url"],
                                call_log.duration =  log["duration"],
                                call_log.missed_calls += 1
                                call_log.save (ignore_permissions=True)
                                frappe.db.commit()  # Commit changes to the database
                            else:
                                create_incoming_call_log (log, user_link)
                                frappe.db.commit()  # Commit changes to the database
                    else:
                        create_incoming_call_log (log, user_link)
                        frappe.db.commit()  # Commit changes to the database
                elif (log["disposition"] == "ANSWERED"):
                    existing_ulog = frappe.get_all(
                                    "Call Log",
                                    filters={
                                        "id": log["id"],
                                    },
                                    fields=["name"]
                                )
                    if not (existing_ulog):
                        existing_log = frappe.get_all(
                                    "Call Log",
                                    filters={
                                        "type": "Incoming",
                                        "from": format_phone_number(log["src"]),
                                        "status": "NO ANSWER",
                                        "followup_status": ["in", ["Pending"]],
                                    },
                                    fields=["name", "start_time"],
                                    order_by="start_time desc"
                                )
                        if (existing_log):
                            for elog in existing_log:
                                call_log = frappe.get_doc ("Call Log", elog.get ("name"))
                                call_log.followup_status = "Completed"
                                call_log.save (ignore_permissions=True)
                                followups = frappe.get_all(
                                    "Followup",
                                    filters={
                                        "call_log": call_log.name,
                                        "status": "Open"
                                    },
                                    fields=["name"]
                                )
                                for followup in followups:
                                    followup_doc = frappe.get_doc ("Followup", followup.get ("name"))
                                    followup_doc.status = "Cancelled"
                                    followup_doc.save (ignore_permissions=True)
                                frappe.db.commit()  # Commit changes to the database
                        create_incoming_call_log (log, user_link)
                        frappe.db.commit()  # Commit changes to the database
                else:
                    create_incoming_call_log (log, user_link)
            else:
                existing_log = frappe.get_all(
                        "Call Log",
                        filters={
                            "type": "OffHour",
                            "from": format_phone_number(log["src"]),
                            "status": "Missed Call",
                            "start_time": [">", now + datetime.timedelta(days=-2)]
                        },
                        fields=["name", "start_time"],
                        order_by="start_time desc"
                    )
                if (existing_log):
                    if (existing_log[0].start_time < created_at):
                        call_log = frappe.get_doc ("Call Log", existing_log[0].get ("name"))
                        call_log.start_time = log["created_at"]
                        call_log.recording_url = log["recording_url"],
                        call_log.duration =  log["duration"],
                        call_log.missed_calls += 1
                        call_log.save (ignore_permissions=True)
                else:
                    create_incoming_call_log (log=log, user_link=user_link, off_hour=off_hour)

            
        
    except Exception as e:
        frappe.log_error(str(e), "Process Call Logs - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}
    
import re 

def format_phone_number(phone_number): 
    # Remove any non-digit characters 
    phone_number = re.sub(r'\D', '', phone_number) 
    # Check if the phone number is 9, 10, 12, or 13 digits long 
    if len(phone_number) == 9: 
        phone_number = '+251' + phone_number 
    elif len(phone_number) == 10: 
        phone_number = '+251' + phone_number[1:] 
    elif len(phone_number) == 12 or (len(phone_number) == 13 and phone_number.startswith('+')): 
        # Add '+' if not present 
        if not phone_number.startswith('+'): 
            phone_number = '+' + phone_number 
    else: 
        return "Invalid phone number length" 
    return phone_number

def create_incoming_call_log (log, user_link=None, off_hour=False):
    try:
        if (not off_hour):
            new_call_log = {
                "doctype": "Call Log",
                "type": "Incoming",
                "id": log["id"],
                "from": format_phone_number(log["src"]),
                "to": log["dst"],
                "employee_user_id": user_link,  # Set call_received_by to user_link (employee_user_id)
                "duration": log["duration"],
                "recording_url": log["recording_url"],
                "status": log["disposition"],
                "start_time": log["created_at"]
            }
            if (log["disposition"] == 'NO ANSWER'):
                new_call_log["missed_calls"] = 1
            frappe.get_doc(new_call_log).insert(ignore_permissions=True)
        else:
            unique_id = str(uuid.uuid4())
            short_id = hashlib.sha256(unique_id.encode()).hexdigest()[:10]
            new_call_log = {
                "doctype": "Call Log",
                "id": short_id,
                "type": "OffHour",
                "from": log["phone"],
                "queue_name": log["queue_name"],
                "status": 'Missed Call',
                "start_time": log["created_at"]
            }
            # Insert the new call log
            frappe.get_doc(new_call_log).insert(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(str(e), "Process Call Logs - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}
    
def create_followup_for_missed_call (call_log, event):
    if (call_log.type == 'Incoming' and call_log.status == 'NO ANSWER'):
        agent = make_assignment ("Missed Call Agents")
        if (agent):
            agent_user_id = frappe.db.get_value ("Employee", agent, "user_id")
            followup = frappe.get_doc ({
                "doctype" : "Followup",
                "event_participants": [
                    {
                        "reference_doctype": "Call Log",
                        "reference_docname": call_log.name,
                    }
                ],
                "subject": "Followup on Missed Call",
                "description" : f"Get back to caller",
                "ends_on": get_due_date(),
                "starts_on": get_due_date() + datetime.timedelta(hours=-1),
                "event_category": "Call",
                "followup_from": "Call Log", 
                "call_log": call_log.name,
                "allocated_to": agent_user_id,
                "followup_trigger": "New Call Log",
                "followup_data": call_log.name,
                "allocated_to": agent_user_id
                # "description" : description
            })
            followup.insert(ignore_permissions=True)

def update_call_log_on_followup_change (followup, event):
    try:
        if followup.call_log:
            old_followup = followup.get_doc_before_save ()
            if (old_followup):
                call_log = frappe.get_doc ("Call Log", followup.call_log)
                call_log_changed = False
                if (followup.followup_status != old_followup.followup_status):  
                    if (call_log):
                        if (followup.followup_status == "Failed to Reach"):
                            call_log.call_log.number_of_retries += 1
                            call_log.followup_status = "Failed to Reach"
                            call_log_changed = True
                            if (call_log.call_log.number_of_retries >= 3):
                                call_log.followup_status = "Not Reachable"
                        elif (followup.followup_status == "Answered"):
                            call_log.followup_status = "Completed"
                            call_log_changed = True
                if (followup.next_followup_date):
                    if (call_log):
                        if (followup.next_followup_date != old_followup.next_followup_date):
                            call_log.next_followup_date = followup.next_followup_date
                            call_log_changed = True
                if (call_log_changed):
                    call_log.save (ignore_permissions=True)

    except Exception as e:
        frappe.log_error(str(e), "Updating Call Log from Followup - General Exception")
        return {"status": "error", "message": "An unexpected error occurred", "details": str(e)}
        

