import datetime
from uuid import UUID

from pydantic import BaseModel, constr, ConfigDict


class CategoryRequestModel(BaseModel):
    name: constr(min_length=1, max_length=256)
    parent_id: UUID | None


class CategoryModel(BaseModel):
    id: UUID | None
    name: constr(min_length=1, max_length=50)
    parent_id: UUID | None
    path: list[UUID] | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryListResponseModel(BaseModel):
    id: UUID
    name: constr(min_length=1, max_length=256)
    parent_id: UUID | None

    model_config = ConfigDict(from_attributes=True)
