from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from homeassistant.core import HomeAssistant

from .const import DEFAULT_SCAN_INTERVAL


class NaturelaCoordinator(
    DataUpdateCoordinator
):

    def __init__(
        self,
        hass: HomeAssistant,
        api,
    ):

        self.api = api

        super().__init__(
            hass,
            logger=None,
            name="Naturela Smart Boiler",
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )


    async def _async_update_data(self):

        result = await self.api.get_status()

        # API returns:
        # {
        # "objectJson":"{...}"
        # }

        import json

        if "objectJson" in result:
            return json.loads(
                result["objectJson"]
            )

        return result