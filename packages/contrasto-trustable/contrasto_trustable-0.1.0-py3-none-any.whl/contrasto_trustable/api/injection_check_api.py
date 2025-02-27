from contrasto_trustable.api.base_api import BaseApi
from contrasto_trustable.api.http_client import SimpleHttpClient
from contrasto_trustable.response_models import (
    ContrastoInjectionResponse,
)


class InjectionCheckApi(BaseApi):
    @property
    def __injection(self) -> SimpleHttpClient:
        return self._build_http_client(endpoint_url="injection/")

    async def check(self, prompt: str) -> str:
        return await self.__injection.get(
            "",
            model=ContrastoInjectionResponse,
            params={"prompt": prompt},
        )
        # if return_raw or not isinstance(parsed_response.message, dict):
        #    return parsed_response
        # for tier, r in sorted(self.config["confidence_tiers"].items(), reverse=True):
        #    if parsed_response.message.probability >= tier:
        #        return r
        # return self.config["default"]
