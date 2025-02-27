from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        coerce_numbers_to_str=False,
        alias_generator=to_camel,
        populate_by_name=True,
    )
