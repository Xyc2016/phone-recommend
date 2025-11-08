from typing import Annotated, Any, TypeVar

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, WithJsonSchema


class BasicModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,  # set to True to allow use ObjectId as a field
    )

    def py(self, *, by_alias=True, **kwargs: Any):
        """这个函数代替model_dump，防止没有使用alias的问题"""
        return self.model_dump(
            by_alias=by_alias,
            **kwargs,
        )


T = TypeVar("T", bound="MongoModel")  # pylint: disable=invalid-name


class MongoModel(BasicModel):
    id: Annotated[
        ObjectId,
        WithJsonSchema({"type": "string"}),
    ] = Field(alias="_id", default_factory=ObjectId)
