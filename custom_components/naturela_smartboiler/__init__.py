from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .api import NaturelaAPI
from .coordinator import NaturelaCoordinator


PLATFORMS = [
    "water_heater",
    "sensor",
    "switch",
    "select",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    api = NaturelaAPI(
        entry.data["email"],
        entry.data["password"],
        entry.data["device_id"],
    )

    await api.login()

    coordinator = NaturelaCoordinator(
        hass,
        api,
    )

    await coordinator.async_config_entry_first_refresh()


    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator


    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS
    )


    return True



async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    unload = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS
    )

    if unload:
        coordinator = hass.data[DOMAIN].pop(
            entry.entry_id
        )

        await coordinator.api.close()


    return unload