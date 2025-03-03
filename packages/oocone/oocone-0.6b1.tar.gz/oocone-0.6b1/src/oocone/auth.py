"""Defines the Auth class."""

from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING

import aiohttp
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from oocone import errors

if TYPE_CHECKING:
    from typing import Any

ROUTE_LOGIN = "/signinForm.php?mode=ok"
BEAUTIFULSOUP_PARSER = "html.parser"

logger = logging.getLogger(__name__)


class Auth:
    """Acquires authentication for the dashboard and makes authenticated requests."""

    def __init__(
        self,
        *,
        websession: aiohttp.ClientSession | None = None,
        base_url: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize."""
        self._base_url = base_url.rstrip("/")
        self.__username = username
        self.__password = password
        self._session = websession or aiohttp.ClientSession()
        self._logged_in = False

    @staticmethod
    def _response_indicates_not_logged_in(response: BeautifulSoup) -> bool:
        if response.title is not None and "abgemeldet" in response.title.text.lower():
            return True
        if response.find("input", {"type": "password"}) is not None:  # noqa: SIM103
            return True

        return False

    async def _login(self) -> None:
        async with self._session.post(
            self._base_url + ROUTE_LOGIN,
            data={"user": self.__username, "passwort": self.__password},
        ) as response:
            response_text = await response.text()

            soup = BeautifulSoup(response_text, features=BEAUTIFULSOUP_PARSER)
            if self._response_indicates_not_logged_in(soup):
                raise errors.AuthenticationFailed

    async def request(
        self, method: str, path: str, *, retry_with_login: bool = True, **kwargs: Any
    ) -> tuple[aiohttp.ClientResponse, BeautifulSoup]:
        """Make a request."""
        try:
            logger.debug("=>       %s %s/%s", method.upper(), self._base_url, path)
            response = await self._session.request(
                method,
                f"{self._base_url}/{path}",
                **kwargs,
            )
        except aiohttp.client_exceptions.ClientError as e:
            raise errors.ConnectionIssue from e

        logger.debug("<= (%s) %s %s/%s", response.status, method.upper(), self._base_url, path)
        soup = BeautifulSoup(await response.text(), BEAUTIFULSOUP_PARSER)

        if self._response_indicates_not_logged_in(soup):
            if retry_with_login:
                await self._login()
                return await self.request(method, path, retry_with_login=False, **kwargs)

            raise errors.AuthenticationFailed

        return (response, soup)


# Some of the responses returned by enocoo trigger a BeautifulSoup warning. So we disable the
# warning, at least for the current module.
warnings.filterwarnings(
    action="ignore",
    category=MarkupResemblesLocatorWarning,
    module=__name__,
    append=True,
)
