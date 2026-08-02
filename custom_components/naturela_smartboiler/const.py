DOMAIN = "naturela_smartboiler"

BASE_URL = "https://iot.naturela-bg.com"

LOGIN_URL = f"{BASE_URL}/Account/Login"

STATUS_URL = (
    f"{BASE_URL}/api/burnertouch/{{device_id}}"
)

COMMAND_URL = (
    f"{BASE_URL}/api/burnertouch/setState"
)

DEFAULT_SCAN_INTERVAL = 30