from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Model


class Core(Model):
    __tablename__ = "core"

    id: Mapped[int] = mapped_column(primary_key=True)
