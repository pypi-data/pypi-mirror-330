from pydantic import BaseModel, ConfigDict, SecretStr, field_validator
import os


class ContrastoApiConfig(BaseModel):
    base_url: str
    timeout: int | None = None
    token: SecretStr | None = None

    @field_validator("token")
    def blank_string(value, field):
        if value is None:
            env_key = os.getenv("CONTRASTO_API_KEY")
            if env_key is not None:
                return SecretStr(env_key)
        return value


class UserConfig(BaseModel):
    """
    A config for the Contrast API.
    """

    confidence_tiers: dict[float, Exception | str]
    default: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
