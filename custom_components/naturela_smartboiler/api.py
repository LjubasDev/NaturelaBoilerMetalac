import aiohttp
import asyncio
from bs4 import BeautifulSoup

from .const import (
    LOGIN_URL,
    STATUS_URL,
    COMMAND_URL
)


class NaturelaAPI:

    def __init__(self, email, password, device_id):
        self.email = email
        self.password = password
        self.device_id = device_id

        self.session = aiohttp.ClientSession()
        self.logged_in = False


    async def close(self):
        await self.session.close()


    async def login(self):

        async with self.session.get(LOGIN_URL) as response:
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
                    "CSRF token not found"
                )

            csrf = token["value"]


        data = {
            "Email": self.email,
            "Password": self.password,
            "rememberMe": "true",
            "__RequestVerificationToken": csrf
        }


        async with self.session.post(
            LOGIN_URL,
            data=data,
            allow_redirects=False
        ) as response:

            if response.status != 302:
                raise Exception(
                     f"Login failed: {response.status}"
                )


        self.logged_in = True


    async def ensure_login(self):

        if not self.logged_in:
            await self.login()



    async def get_status(self):

        await self.ensure_login()

        url = STATUS_URL.format(
            device_id=self.device_id
        )

        async with self.session.get(url) as response:

            if response.status == 401:
                self.logged_in = False
                await self.login()
                return await self.get_status()


            data = await response.json()

            return data



    async def set_state(
        self,
        state=None,
        temperature=None,
        heater=None
    ):

        await self.ensure_login()

        payload = {
            "deviceId": self.device_id
        }

        if state is not None:
            payload["state"] = state

        if temperature is not None:
            payload["temperature"] = temperature

        if heater is not None:
            payload["heater"] = heater


        async with self.session.post(
            COMMAND_URL,
            json=payload
        ) as response:

            return await response.text()