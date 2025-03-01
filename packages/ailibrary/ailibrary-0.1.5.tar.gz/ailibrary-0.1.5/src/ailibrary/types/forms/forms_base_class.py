from typing import Any
from ..shared.base import CustomBaseModel
from pydantic import Field, ConfigDict

class FormsBaseClass(CustomBaseModel):
    model_config = ConfigDict(populate_by_name=True, by_alias=True)
    schema_data: Any = Field(default=None, alias="schema")

    @property
    def schema(self) -> Any:
        return self.schema_data

    @schema.setter
    def schema(self, value: Any) -> None:
        self.schema_data = value

    def model_dump(self, *args, **kwargs):
        kwargs['exclude_none'] = True
        kwargs["by_alias"] = True
        return super().model_dump(*args, **kwargs)