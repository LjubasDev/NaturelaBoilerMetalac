import aiohttp
import logging
import json

from bs4 import BeautifulSoup

from .const import (
    LOGIN_URL,
    STATUS_URL,
    COMMAND_URL,
)


_LOGGER = logging.getLogger(__name__)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/150 Safari/537.36"
    ),
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://iot.naturela-bg.com/Account/Login",
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
                    "name":
                    "__RequestVerificationToken"
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

            "rememberMe": "on",

            "__RequestVerificationToken": csrf
        }



            async with self.session.post(
                LOGIN_URL,
                data=payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
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


        _LOGGER.debug(
            "Getting boiler status: %s",
            url
        )


        async with self.session.get(
            url
        ) as response:


            content_type = response.headers.get(
                "Content-Type"
            )


            text = await response.text()


            _LOGGER.warning(
                "Naturela response type: %s",
                content_type
            )


            _LOGGER.warning(
                "Naturela response body: %s",
                text
            )



            if response.status == 401:

                self.logged_in = False

                await self.login()

                return await self.get_status()



            try:

                return json.loads(
                    text
                )


            except Exception:


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


        payload = {

            "deviceId":
            self.device_id

        }


        if state is not None:

            payload["state"] = state


        if temperature is not None:

            payload["temperature"] = temperature


        if heater is not None:

            payload["heater"] = heater



        _LOGGER.debug(
            "Sending command: %s",
            payload
        )



        async with self.session.post(
            COMMAND_URL,
            json=payload
        ) as response:


            text = await response.text()


            _LOGGER.debug(
                "Command response: %s",
                text
            )


            return text
