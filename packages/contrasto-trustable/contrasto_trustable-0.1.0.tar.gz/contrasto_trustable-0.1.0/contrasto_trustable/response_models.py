from pydantic import BaseModel, Field, TypeAdapter


# injection API response models
class GenericInjectionResponse(BaseModel):
    message: str = Field(description="The message from the API")


class ContrastoMessageResponse(BaseModel):
    label: str = Field(
        description="The label of the injection. Can be 'injection' or 'safe'."
    )
    probability: float = Field(
        description="The probability of the injection. Can be a value between 0 and 1."
    )


class ContrastoInjectionResponse(BaseModel):
    prompt: str = Field(description="The prompt that was checked.")
    message: ContrastoMessageResponse = Field(description="The message from the API.")


output_schema: TypeAdapter[ContrastoInjectionResponse | GenericInjectionResponse] = (
    TypeAdapter(ContrastoInjectionResponse | GenericInjectionResponse)
)
