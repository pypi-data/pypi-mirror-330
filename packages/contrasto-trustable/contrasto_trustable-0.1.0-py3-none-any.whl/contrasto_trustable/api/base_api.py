from typing import TypeVar
from pydantic import BaseModel, ConfigDict, Field
import logging

from contrasto_trustable.api.http_client import SimpleHttpClient
from contrasto_trustable.config import ContrastoApiConfig


logger = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound=BaseModel)
TData = TypeVar("TData", bound=BaseModel)


class ClientConfig(BaseModel):
    base_url: str = Field(
        ...,
        description="base url that will prefix the url fragment sent via the client",
    )
    headers: dict = Field(..., description="http headers sent to the API server")

    model_config = ConfigDict(extra="allow")


class BaseApi:
    """
    The base class for Contrasto Trustable APIs.
    """

    def __init__(self, config: ContrastoApiConfig):
        self.config = config

    def _build_http_client(
        self, endpoint_url: str = "", extra_headers: dict | None = None
    ):
        headers = {
            "Content-Type": "application/json",
            **(extra_headers or {}),
        }
        if self.config.token:
            headers["Authorization"] = f"Bearer {self.config.token.get_secret_value()}"

        return SimpleHttpClient(
            client_config=self.config,
            base_url=endpoint_url,
            headers=headers,
            timeout=self.config.timeout,
        )
