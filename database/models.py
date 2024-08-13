import enum
from typing import Annotated
from sqlalchemy import func, ForeignKey

from database.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(insert_default=func.now())]


# Модель описывает таблицу Users в бд
class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]


# Модель описывает таблицу Items в бд
class Item(Base):
    __tablename__ = 'items'

    id: Mapped[intpk]
    title: Mapped[str]
    descr: Mapped[str]
    cost: Mapped[int]
    photo_src: Mapped[str]
    created_at: Mapped[created_at]

    tags: Mapped[list['Tag']] = relationship(
        back_populates='items',
        secondary='tagstoitems'
    )


# Модель описывает таблицу tags в бд
class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[intpk]
    title: Mapped[str]

    items: Mapped[list['Item']] = relationship(
        back_populates='tags',
        secondary='tagstoitems'
    )


# Модель описывает связь таблиц Items и Tags
class TagsToItems(Base):
    __tablename__ = 'tagstoitems'

    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tags.id', ondelete='CASCADE'),
        primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey('items.id', ondelete='CASCADE'),
        primary_key=True
    )




