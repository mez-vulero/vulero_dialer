## Vulero Dialer

Dialer Modal for Ethiopia

### SIP Middleware

The `SipMiddleware` module provides a simple wrapper around the PBX HTTP API so
other projects can interact with the SIP server without relying on Frappe.  The
middleware can fetch connection details, manage queue membership and retrieve
call logs.

Example usage:

```python
from vulero_dialer import PBXConfig, SipMiddleware

config = PBXConfig(organization_id="ORG", api_key="API_KEY")
client = SipMiddleware(config)

# Fetch SIP connection details
info = client.get_connection_details("1001")

# Join a queue
client.add_to_queue(queue_name="support", extension="1001")
```

#### License

mit
