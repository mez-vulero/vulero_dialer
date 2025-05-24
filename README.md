## Vulero Dialer

Dialer Modal for Ethiopia

### SIP Middleware

The `SipMiddleware` module provides a simple wrapper around the PBX HTTP API so
projects can interact with the SIP server without relying on Frappe. It can
fetch connection details, manage queue membership and retrieve call logs.

Basic usage inside this app:

```python
from vulero_dialer import PBXConfig, SipMiddleware

config = PBXConfig(organization_id="ORG", api_key="API_KEY")
client = SipMiddleware(config)
```

### Standalone Usage

To integrate with any technology stack, copy the `pbx_middleware` package or
install this repository as a dependency and import from `pbx_middleware`:

```python
from pbx_middleware import PBXConfig, SipMiddleware

client = SipMiddleware(PBXConfig("ORG", "API_KEY"))
info = client.get_connection_details("1001")
```

#### License

mit
