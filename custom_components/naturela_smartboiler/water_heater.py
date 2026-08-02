from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)

from homeassistant.const import (
    UnitOfTemperature,
)

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
            NaturelaWaterHeater(coordinator)
        ]
    )


class NaturelaWaterHeater(
    CoordinatorEntity,
    WaterHeaterEntity
):

    _attr_has_entity_name = True

    _attr_supported_features = (
        WaterHeaterEntityFeature
        .TARGET_TEMPERATURE
    )

    _attr_temperature_unit = (
        UnitOfTemperature.CELSIUS
    )


    def __init__(self, coordinator):

        super().__init__(coordinator)

        self.coordinator = coordinator

        self._attr_name = (
            "Smart Boiler"
        )

        self._attr_unique_id = (
            "naturela_smartboiler_main"
        )


    @property
    def current_temperature(self):

        return self.coordinator.data.get(
            "WH_TempL"
        )


    @property
    def target_temperature(self):

        return self.coordinator.data.get(
            "SetTemp"
        )


    async def async_set_temperature(
        self,
        **kwargs
    ):

        temperature = kwargs.get(
            "temperature"
        )

        await self.coordinator.api.set_state(
            temperature=temperature
        )

        await self.coordinator.async_request_refresh()



    @property
    def current_operation(self):

        states = {
            0: "Off",
            1: "Heating",
            2: "Smart",
            3: "Self Learning",
            4: "Timer",
        }

        return states.get(
            self.coordinator.data.get("State"),
            "Unknown"
        )