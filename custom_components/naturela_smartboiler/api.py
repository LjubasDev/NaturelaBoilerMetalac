import aiohttp
import logging
import json

from bs4 import BeautifulSoup

from .const import (
    LOGIN_URL,
    STATUS_URL,
    SET_STATE_URL,
    SET_HEATER_URL,
    SET_TEMPERATURE_URL,
)


_LOGGER = logging.getLogger(__name__)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/150 Safari/537.36"
    ),
    "Accept": "*/*",
    "Referer": "https://iot.naturela-bg.com/",
}


class NaturelaAPI:

    def __init__(
        self,
        email,
        password,
        device_id
    ):
        self.email = email
        self.password = password
        self.device_id = device_id
        self.command_device_id = None

        self.session = aiohttp.ClientSession(
            headers=HEADERS
        )

        self.logged_in = False


    async def close(self):
        await self.session.close()



    async def login(self):

        _LOGGER.info("Logging into Naturela")


        async with self.session.get(
            LOGIN_URL
        ) as response:

            html = await response.text()


        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        token = soup.find(
            "input",
            {
                "name": "__RequestVerificationToken"
            }
        )


        if not token:
            raise Exception(
                "CSRF token missing"
            )


        csrf = token["value"]


        payload = {
            "Email": self.email,
            "Password": self.password,
            "rememberMe": "true",
            "__RequestVerificationToken": csrf
        }


        async with self.session.post(
            LOGIN_URL,
            data=payload,
            allow_redirects=False
        ) as response:


            _LOGGER.warning(
                "Login response: %s",
                response.status
            )


            if response.status not in (302,303):

                text = await response.text()

                raise Exception(
                    f"Login failed: {text}"
                )


        self.logged_in = True

        _LOGGER.info(
            "Naturela login successful"
        )



    async def ensure_login(self):

        if not self.logged_in:
            await self.login()



    async def get_status(self):

        await self.ensure_login()


        url = STATUS_URL.format(
            device_id=self.device_id
        )


        async with self.session.get(
            url
        ) as response:


            text = await response.text()


            _LOGGER.debug(
                "Status response: %s",
                text
            )


            if response.status == 401:

                self.logged_in = False

                await self.login()

                return await self.get_status()



            if not text.strip():

                raise Exception(
                    "Naturela returned empty response"
                )


            try:

                data = json.loads(text)
                device_data = data

                if isinstance(data, dict) and isinstance(
                    data.get("objectJson"), str
                ):
                    try:
                        device_data = json.loads(data["objectJson"])
                    except json.JSONDecodeError:
                        device_data = data

                if isinstance(device_data, dict):
                    command_device_id = device_data.get("DeviceID")
                    if command_device_id is not None:
                        self.command_device_id = str(command_device_id)

                return data

            except Exception:

                raise Exception(
                    f"Invalid JSON: {text}"
                )



    async def set_state(
        self,
        state
    ):

        await self.ensure_login()


        payload = {
            "deviceId": self.command_device_id or self.device_id,
            "state": state
        }


        _LOGGER.info(
            "Setting boiler state: %s",
            payload
        )


        async with self.session.post(
            SET_STATE_URL,
            json=payload
        ) as response:


            result = await response.text()


            _LOGGER.warning(
                "Naturela setState HTTP %s: %s",
                response.status,
                result[:300]
            )

            response.raise_for_status()


            return result


    async def set_heater(
        self,
        heater
    ):

        await self.ensure_login()

        payload = {
            "deviceId": self.command_device_id or self.device_id,
            "heater": 1 if heater else 0
        }

        _LOGGER.info(
            "Setting boiler heater: %s",
            payload
        )

        async with self.session.post(
            SET_HEATER_URL,
            json=payload
        ) as response:

            result = await response.text()

            _LOGGER.warning(
                "Naturela setHeater HTTP %s: %s",
                response.status,
                result[:300]
            )

            response.raise_for_status()

            return result



    async def set_temperature(
        self,
        temperature
    ):

        await self.ensure_login()


        payload = {
            "deviceId": self.command_device_id or self.device_id,
            "temperature": temperature
        }


        _LOGGER.info(
            "Setting temperature: %s",
            payload
        )


        async with self.session.post(
            SET_TEMPERATURE_URL,
            json=payload
        ) as response:


            result = await response.text()


            _LOGGER.warning(
                "Naturela setTemperature HTTP %s: %s",
                response.status,
                result[:300]
            )

            response.raise_for_status()


            return result
