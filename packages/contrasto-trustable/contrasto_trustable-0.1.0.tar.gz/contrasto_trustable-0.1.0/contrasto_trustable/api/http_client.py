from typing import Type, TypeVar
from pydantic import BaseModel
import logging
import aiohttp

from contrasto_trustable.config import ContrastoApiConfig
from contrasto_trustable.exceptions import handle_api_error, handle_client_error

logger = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound=BaseModel)
TData = TypeVar("TData", bound=BaseModel)


class SimpleHttpClient:
    """
    Base client for Contrasto APIs. For now, only supports GET requests.
    """

    def __init__(
        self,
        client_config: ContrastoApiConfig,
        headers: dict,
        base_url: str = "",
        timeout: int | None = None,
    ):
        self._client_config = client_config
        self._headers = headers

        # the endpoind groups to append to the config base url
        self._base_url = base_url
        if timeout is not None:
            self._client_config.timeout = timeout

    def _log_request(self, url: str, method: str) -> None:
        logger.debug(f"Sending HTTP request: {method} {url}")

    def _log_response(self, url: str, method: str, status: int) -> None:
        logger.debug(f"Received HTTP response: {method} {url}, status: {status}")

    def _prepare_json(
        self, json: TData | dict | list | None = None
    ) -> TData | dict | list | None:
        if json is None:
            return None

        if isinstance(json, dict):
            return json

        if isinstance(json, list):
            return [self._prepare_json(item) for item in json]

        return json.dict(exclude_unset=True, exclude_none=True)

    @handle_client_error
    async def get(self, url, model: Type[TModel], **kwargs) -> TModel:
        url = f"{self._base_url}{url}"
        async with aiohttp.ClientSession(
            base_url=self._client_config.base_url,
            headers=self._headers,
            timeout=aiohttp.ClientTimeout(total=self._client_config.timeout),
        ) as client:
            self._log_request(url, "GET")
            async with client.get(url, **kwargs) as response:
                await handle_api_error(response)
                self._log_response(url, "GET", response.status)
                data = await response.json()
                return model.model_validate(data)
