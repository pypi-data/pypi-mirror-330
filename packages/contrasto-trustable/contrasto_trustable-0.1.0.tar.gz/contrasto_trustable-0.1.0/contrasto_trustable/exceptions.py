from typing import Optional
import aiohttp
import functools
import logging

logger = logging.getLogger(__name__)

DEFAULT_SUPPORT_LINK = "https://contrastoai.com/support"


class ContrastoError(Exception):
    """Contrasto base exception"""


class ContrastoConnectionError(ContrastoError):
    """Contrasto connection exception"""

    def __init__(self, message: str, *, error: Optional[aiohttp.ClientError] = None):
        super().__init__(message)
        self.original_error = error


class ContrastoContextError(ContrastoError):
    """
    The `ContrastoContextError` occurs when an API method is called with insufficient context
    (missing required environment, project, or organization information).
    """


class ContrastoApiError(ContrastoError):
    """
    Wraps an error HTTP Response that occurred during a Contrasto REST API request.
    """

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        body: Optional[dict] = None,
    ):
        super().__init__()
        self._response = response
        self._body = body

    def _get_message(self) -> str:
        return f"{self.status_code} API Error: {self.details}"

    def __str__(self):
        return self._get_message()

    @property
    def message(self) -> str:
        return self._get_message()

    @property
    def response(self) -> aiohttp.ClientResponse:
        return self._response

    @property
    def details(self) -> Optional[dict]:
        return self._body

    @property
    def status_code(self) -> int:
        return self._response.status


class ContrastoPromptError(ContrastoApiError):
    """
    Prompt error response from the Contrasto API.
    """


class ContrastoValidationError(ContrastoApiError):
    """
    Validation error response from the Contrasto API.
    """


class ContrastoNotFoundError(ContrastoApiError):
    """
    Object not found response from the Contrasto API.
    """


class ContrastoAlreadyExistsError(ContrastoApiError):
    """
    Object already exists response from the Contrasto API.
    """


async def handle_api_error(response: aiohttp.ClientResponse):
    if 200 <= response.status < 400:
        return

    try:
        json = await response.json()
    except aiohttp.ContentTypeError as e:
        text = await response.text()
        raise ContrastoApiError(response, {"details": text[:100]}) from e

    match response.status:
        case 422:
            raise ContrastoValidationError(response, json)
        case 409:
            raise ContrastoAlreadyExistsError(response, json)
        case 404:
            raise ContrastoNotFoundError(response, json)
        case _:
            raise ContrastoApiError(response, json)


def handle_client_error(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientError as err:
            logger.error("got client error while sending an http request: %s", err)
            raise ContrastoConnectionError(f"{err}", error=err) from err

    return wrapped
