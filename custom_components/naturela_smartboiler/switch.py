from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from homeassistant.helpers.update_coordinator import CoordinatorEntity



async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]


    async_add_entities(
        [
            BoostSwitch(coordinator)
        ]
    )



class BoostSwitch(
    CoordinatorEntity,
    SwitchEntity
):

    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator
        )

        self.coordinator = coordinator

        self._attr_name = (
            "Boiler Boost"
        )

        self._attr_unique_id = (
            "naturela_boost"
        )


    @property
    def is_on(self):

        return self.coordinator.data.get(
            "BoostHeating",
            False
        )


    async def async_turn_on(self):

        await self.coordinator.api.set_state(
            heater=True
        )

        await self.coordinator.async_request_refresh()



    async def async_turn_off(self):

        await self.coordinator.api.set_state(
            heater=False
        )

        await self.coordinator.async_request_refresh()