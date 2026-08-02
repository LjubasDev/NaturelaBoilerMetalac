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
            BoilerModeSelect(coordinator)
        ]
    )


class BoilerModeSelect(
    CoordinatorEntity,
    SelectEntity
):

    _attr_has_entity_name = True


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator
        )

        self.coordinator = coordinator

        self._attr_name = "Mode"

        self._attr_unique_id = (
            "naturela_smartboiler_mode"
        )

        self._attr_options = list(
            MODES.values()
        )


    @property
    def current_option(self):

        state = self.coordinator.data.get(
            "State"
        )

        return MODES.get(
            state,
            "Unknown"
        )


    async def async_select_option(
        self,
        option
    ):

        reverse_modes = {
            value: key
            for key, value in MODES.items()
        }

        state = reverse_modes.get(
            option
        )


        if state is None:
            return


        await self.coordinator.api.set_state(
            state
        )


        await self.coordinator.async_request_refresh()
