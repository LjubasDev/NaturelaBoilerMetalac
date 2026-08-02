import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from homeassistant.core import HomeAssistant

from .const import DEFAULT_SCAN_INTERVAL


_LOGGER = logging.getLogger(__name__)


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
            logger=_LOGGER,
            name="Naturela Smart Boiler",
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )
