from typing import Protocol, runtime_checkable

from pydantic import SecretStr

from contrasto_trustable.api.api_client import ContrastoTrustableApiClient
from contrasto_trustable.config import ContrastoApiConfig, UserConfig


@runtime_checkable
class Trustable(Protocol):
    """
    Protocol defining the interface for Contrasto clients.
    Can be implemented by remote API clients or local containerized solutions.
    """

    def check_inject(self, input: str) -> str | Exception:
        """
        Detect if the input is an injection.

        Args:
            input: The string to check for injection attempts

        Returns:
            str | Exception: The result of the injection check
        """
        ...


class ContrastoTrustable:
    """
    A client for the Contrast API.
    """

    def __init__(
        self,
        api_key: SecretStr | None = None,
        api_url: str = "https://api.contrastoai.com/api/trustable/",
        overrided_user_config: UserConfig | None = None,
    ):
        self._config = ContrastoApiConfig(
            base_url=api_url,
            token=api_key,
        )

        self._api = ContrastoTrustableApiClient(self._config, overrided_user_config)

    @property
    def config(self):
        """
        Access the SDK configuration using this property.
        Once the SDK is initialized, the configuration is read-only.

        Usage example:

            contrasto = ContrastoTrustable(config)
            pdp_url = contrasto.config.pdp
        """
        return self._config.model_copy()

    @property
    def api(self) -> ContrastoTrustableApiClient:
        """
        Access the Contrasto Trustable REST API using this property.

        Usage example:

            contrasto = ContrastoTrustable(token="<YOUR_API_KEY>")
            await contrasto.api.injection_check.check(...)
        """
        return self._api


class MockClient:
    """
    A mock client for the Contrast API.
    """

    def check_inject(self, input: str) -> str | Exception:
        return ValueError(input)
