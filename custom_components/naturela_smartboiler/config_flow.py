import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class NaturelaConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN
):

    VERSION = 1


    async def async_step_user(
        self,
        user_input=None
    ):

        if user_input:

            return self.async_create_entry(
                title="Naturela Smart Boiler",
                data=user_input
            )


        schema = vol.Schema(
            {
                vol.Required(
                    "email"
                ): str,

                vol.Required(
                    "password"
                ): str,

                vol.Required(
                    "device_id",
                    default=""
                ): str,
            }
        )


        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )