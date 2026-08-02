from homeassistant.components.select import SelectEntity

from .const import DOMAIN
from homeassistant.helpers.update_coordinator import CoordinatorEntity


MODES = {
    0: "Off",
    1: "Heating",
    2: "Smart",
    3: "Self Learning",
    4: "Timer",
}



async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            BoilerModeSelect(
                coordinator
            )
        ]
    )



class BoilerModeSelect(
    CoordinatorEntity,
    SelectEntity
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
            "Boiler Mode"
        )

        self._attr_options = list(
            MODES.values()
        )



    @property
    def current_option(self):

        return MODES.get(
            self.coordinator.data.get(
                "State"
            )
        )


    async def async_select_option(
        self,
        option
    ):

        state = list(MODES.keys())[
            list(MODES.values()).index(option)
        ]


        await self.coordinator.api.set_state(
            state=state
        )

        await self.coordinator.async_request_refresh()