from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ItemBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)
    price: float = None
    category_id: UUID | None = None
    #image_id: UUID | None = None


class ItemCreate(ItemBase):
    ...


class ItemUpdate(ItemBase):
    ...


class Item(ItemBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


