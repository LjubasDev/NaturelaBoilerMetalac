from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN
from homeassistant.helpers.update_coordinator import CoordinatorEntity


SENSORS = {
    "WH_TempL": (
        "Water Temperature",
        "°C",
    ),

    "EnergyD": (
        "Energy Day",
        "kWh",
    ),

    "EnergyN": (
        "Energy Night",
        "kWh",
    ),

    "SavedEnergy": (
        "Saved Energy",
        "kWh",
    ),

    "ErrorFlag": (
        "Error Code",
        None,
    ),

    "EcoInd": (
        "Eco Index",
        None,
    ),

}


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]


    entities = []

    for key, values in SENSORS.items():

        entities.append(
            NaturelaSensor(
                coordinator,
                key,
                values[0],
                values[1]
            )
        )


    async_add_entities(
        entities
    )



class NaturelaSensor(
    CoordinatorEntity,
    SensorEntity
):

    def __init__(
        self,
        coordinator,
        key,
        name,
        unit
    ):

        super().__init__(
            coordinator
        )

        self.key = key

        self._attr_name = (
            f"Naturela {name}"
        )

        self._attr_native_unit_of_measurement = unit


        self._attr_unique_id = (
            f"naturela_{key}"
        )


    @property
    def native_value(self):

        return self.coordinator.data.get(
            self.key
        )