from homeassistant.components.diagnostics import async_redact_data

from .const import DOMAIN


TO_REDACT = {
    "deviceId",
}


async def async_get_config_entry_diagnostics(
    hass,
    config_entry,
):

    coordinator = hass.data[DOMAIN][config_entry.entry_id]


    return {
        "device": async_redact_data(
            coordinator.data,
            TO_REDACT
        )
    }