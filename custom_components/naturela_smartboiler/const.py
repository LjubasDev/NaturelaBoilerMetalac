DOMAIN = "naturela_smartboiler"


BASE_URL = "https://iot.naturela-bg.com"


LOGIN_URL = (
    BASE_URL +
    "/Account/Login"
)


STATUS_URL = (
    BASE_URL +
    "/api/smartboiler/{device_id}"
)


SET_TEMPERATURE_URL = (
    BASE_URL +
    "/api/smartboiler/setTemperature"
)


SET_STATE_URL = (
    BASE_URL +
    "/api/smartboiler/setState"
)


SET_HEATER_URL = (
    BASE_URL +
    "/api/smartboiler/setHeater"
)


# Home Assistant update interval
DEFAULT_SCAN_INTERVAL = 30
