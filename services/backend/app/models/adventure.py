import uuid

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from services.backend.app.db.session import Base
from services.backend.app.models.mixins import Timestamp


class Adventure(Timestamp, Base):
    __tablename__ = "adventures"

    id = Column(UUID(as_uuid=uuid), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(250))
    user_id = Column(UUID, ForeignKey("users.id"), unique=False)

    items = relationship("Item", secondary="adventure_groups", back_populates="adventures")


class AdventureGroup(Base):
    __tablename__ = "adventure_groups"

    item_id = Column(UUID, ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    adventure_id = Column(UUID, ForeignKey("adventures.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

