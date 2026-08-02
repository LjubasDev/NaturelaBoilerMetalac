DOMAIN = "naturela_smartboiler"

BASE_URL = "https://iot.naturela-bg.com"

LOGIN_URL = f"{BASE_URL}/Account/Login"

STATUS_URL = (
    f"{BASE_URL}/api/smartboiler/{{device_id}}"
)

SET_STATE_URL = (
    f"{BASE_URL}/api/smartboiler/setState"
)

SET_TEMPERATURE_URL = (
    f"{BASE_URL}/api/smartboiler/setTemperature"
)

DEFAULT_SCAN_INTERVAL = 30
