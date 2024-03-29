from sqlalchemy import Boolean, Column, ForeignKey, String, Float, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid

from .mixins import Timestamp
from ..db.session import Base


class Item(Timestamp, Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(250))
    price = Column(Float, index=True)
    is_active = Column(Boolean, default=False)
    item_picture = Column(String, nullable=True)
    image_id = Column(UUID(as_uuid=True), nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"), unique=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    owner = relationship("User", back_populates="item")
    image = relationship("Image", back_populates="item")
    adventures = relationship("Adventure", secondary="adventure_groups", back_populates="items", cascade="all, delete")
    category = relationship("Category", backref="items")


class Image(Timestamp, Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), unique=False, index=True, nullable=True)
    file = Column(LargeBinary)
    item_id = Column(UUID, ForeignKey("items.id"), unique=True, nullable=False)

    item = relationship("Item", back_populates="image")


class Category(Timestamp, Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
