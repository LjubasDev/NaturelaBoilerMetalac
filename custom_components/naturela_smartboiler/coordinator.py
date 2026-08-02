import logging
import json
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from homeassistant.core import HomeAssistant

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
            logger=_LOGGER,
            name="Naturela Smart Boiler",
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )


    async def _async_update_data(self):

        try:
            result = await self.api.get_status()

            _LOGGER.debug(
                "Naturela raw response: %s",
                result
            )

            if "objectJson" in result:
                return json.loads(
                    result["objectJson"]
                )

            return result


        except Exception as err:

            _LOGGER.error(
                "Failed to update Naturela data: %s",
                err
            )

            raise
