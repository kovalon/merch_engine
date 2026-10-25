import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, func, Uuid, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base


class CategoryTable(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"), nullable=True)
    parent = relationship(lambda: CategoryTable, remote_side=id, backref="children")
    path: Mapped[list[UUID]] = mapped_column(ARRAY(Uuid), nullable=True, default=[])
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
