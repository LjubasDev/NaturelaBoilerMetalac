import aiohttp
import logging
import json

from bs4 import BeautifulSoup

from .const import (
    LOGIN_URL,
    STATUS_URL,
    SET_TEMPERATURE_URL,
    SET_STATE_URL,
    SET_HEATER_URL,
)


_LOGGER = logging.getLogger(__name__)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/150 Safari/537.36"
    ),
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
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

        self.session = aiohttp.ClientSession(
            headers=HEADERS
        )

        self.logged_in = False


    async def close(self):

        await self.session.close()



    async def login(self):

        _LOGGER.info(
            "Logging into Naturela"
        )


        # Get login page and extract CSRF token
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
                "Naturela CSRF token not found"
            )


        csrf = token.get(
            "value"
        )


        payload = {

            "Email": self.email,

            "Password": self.password,

            "rememberMe": "true",

            "__RequestVerificationToken": csrf
        }


        _LOGGER.warning(
            "Trying login with email: %s",
            self.email
        )


        _LOGGER.warning(
            "CSRF token length: %s",
            len(csrf)
        )


        # Send login form
        async with self.session.post(
            LOGIN_URL,
            data=payload,
            headers={
                "Content-Type":
                "application/x-www-form-urlencoded"
            },
            allow_redirects=False
        ) as response:


            _LOGGER.warning(
                "Login response: %s",
                response.status
            )


            if response.status not in (
                302,
                303
            ):

                text = await response.text()


                _LOGGER.warning(
                    "Login failed body: %s",
                    text
                )


                raise Exception(
                    "Naturela login failed"
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


        _LOGGER.info(
            "Requesting boiler data: %s",
            url
        )


        async with self.session.get(
            url,
            headers={
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Referer": "https://iot.naturela-bg.com/",
            }
        ) as response:


            text = await response.text()


            _LOGGER.warning(
                "Naturela status HTTP: %s",
                response.status
            )


            _LOGGER.warning(
                "Naturela content type: %s",
                response.headers.get(
                    "Content-Type"
                )
            )


            _LOGGER.warning(
                "Naturela raw response: %s",
                text
            )


            if response.status == 401:

                self.logged_in = False

                await self.login()

                return await self.get_status()



            if not text:

                raise Exception(
                    "Naturela returned empty response"
                )


            try:

                return json.loads(
                    text
                )


            except json.JSONDecodeError:

                raise Exception(
                    "Naturela returned invalid JSON:\n"
                    + text
                )



            async def set_state(
                self,
                state=None,
                temperature=None,
                heater=None
            ):
            
                await self.ensure_login()
            
            
                if temperature is not None:
            
                    payload = {
                        "deviceId": self.device_id,
                        "temperature": temperature
                    }
            
                    url = SET_TEMPERATURE_URL
            
            
                elif state is not None:
            
                    payload = {
                        "deviceId": self.device_id,
                        "state": state
                    }
            
                    url = SET_STATE_URL
            
            
                elif heater is not None:
            
                    payload = {
                        "deviceId": self.device_id,
                        "heater": heater
                    }
            
                    url = SET_HEATER_URL
            
            
                else:
            
                    return
            
            
            
                _LOGGER.warning(
                    "Sending SmartBoiler command: %s",
                    payload
                )
            
            
                async with self.session.post(
                    url,
                    json=payload
                ) as response:
            
            
                    text = await response.text()
            
            
                    _LOGGER.warning(
                        "SmartBoiler command response %s: %s",
                        response.status,
                        text
                    )
            
            
                    return text
