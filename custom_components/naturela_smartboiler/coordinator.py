import logging
import json
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SCAN_INTERVAL


_LOGGER = logging.getLogger(__name__)


class NaturelaCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass: HomeAssistant,
        api,
    ):
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name="Naturela Smart Boiler",
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )


    async def _async_update_data(self):

        _LOGGER.warning(
            "Naturela update method running"
        )

        response = await self.api.get_status()

        _LOGGER.debug(
            "Naturela response: %s",
            response
        )

        if "objectJson" in response:
            return json.loads(
                response["objectJson"]
            )

        return response
