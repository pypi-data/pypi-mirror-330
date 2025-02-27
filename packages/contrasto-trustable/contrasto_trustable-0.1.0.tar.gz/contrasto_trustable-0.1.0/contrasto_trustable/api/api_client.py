from pydantic import SecretStr
import requests

from contrasto_trustable.api.injection_check_api import InjectionCheckApi
from contrasto_trustable.config import ContrastoApiConfig, UserConfig


class ContrastoTrustableApiClient:
    def __init__(
        self,
        config: ContrastoApiConfig,
        overrided_user_config: UserConfig | None = None,
    ):
        """
        Constructs a new instance of the ApiClient class with the specified SDK configuration.

        Args:
            config: The configuration for the Contrast API.
        """

        self._injection_check = InjectionCheckApi(config)

        if overrided_user_config is None:
            self._user_config = self._get_remote_config(config.base_url, config.token)
        else:
            self._user_config = overrided_user_config

    @property
    def injection_check(self) -> InjectionCheckApi:
        """
        API for managing injection check.
        See: https://api.contrastoai.com/api/trustable/redoc#tag/InjectionCheck
        """
        return self._injection_check

    def _get_remote_config(
        self, base_url: str, token: SecretStr | None = None
    ) -> UserConfig:
        """
        Get the config for the Contrast API.
        """
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(
            f"{base_url}/config",
            headers=headers,
        )

        if response.status_code != 200:
            raise ValueError(f"Failed to get config: {response.text}")

        config_data = response.json()
        config = UserConfig.model_validate(config_data)
        return config
