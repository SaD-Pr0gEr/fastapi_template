from sqlalchemy import (
    insert, update, Update, select, Select, delete, Delete, exists
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from sqlalchemy.sql.functions import random


class Repository:
    model = None

    def __init__(self, session: AsyncSession | Session):
        self.session = session

    def get_random_model_stmt(self, **filter_by) -> Select:
        return (
            select(self.model)
            .filter_by(**filter_by)
            .order_by(random())
            .limit(1)
        )

    def add_one_stmt(self, data: dict) -> ReturningInsert:
        stmt = insert(self.model).values(**data).returning(self.model)
        return stmt

    def edit_one_stmt(self, id: int, data: dict) -> ReturningUpdate:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(self.model)
        )
        return stmt

    def edit_by_filter_stmt(self, filters: dict, data: dict) -> Update:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(**filters)
            .returning(self.model)
        )
        return stmt

    def get_all_stmt(self) -> Select:
        stmt = select(self.model)
        return stmt

    def filter_by_stmt(self, **filter_by) -> Select:
        stmt = select(self.model).filter_by(**filter_by)
        return stmt

    def delete_stmt(self, **filter_by) -> Delete:
        stmt = delete(self.model).filter_by(**filter_by)
        return stmt

    def add_one(self, data: dict[str, int | float | str | bool | None | dict]):
        return (
            self.session.execute(
                self.add_one_stmt(data)
            ).scalar_one_or_none()
        )

    def edit_one(
            self, id: int,
            data: dict[str, int | float | str | bool | None | dict]
    ):
        return (
            self.session.execute(
                self.edit_one_stmt(id, data)
            ).scalar_one_or_none()
        )

    def edit_by_filter(self, filters: dict, data: dict):
        return self.session.execute(
            self.edit_by_filter_stmt(filters, data)
        ).scalars().all()

    def get_all(self):
        return self.session.execute(self.get_all_stmt()).scalars().all()

    def get_random_model(self, **filter_by):
        return self.session.execute(
            self.get_random_model_stmt(**filter_by)
        ).scalar_one_or_none()

    def filter_by(self, one: bool = False, **filter_by):
        result = self.session.execute(
            self.filter_by_stmt(**filter_by)
        ).scalars()
        return result.first() if one else result.all()

    def delete(self, **filter_by):
        self.session.execute(self.delete_stmt(**filter_by))

    async def add_one_async(
            self, data: dict[str, int | float | str | bool | None | dict]
    ):
        result = await self.session.execute(self.add_one_stmt(data))
        return result.scalar_one_or_none()

    async def edit_one_async(
            self, id: int,
            data: dict[str, int | float | str | bool | None | dict]
    ):
        result = await self.session.execute(self.edit_one_stmt(id, data))
        return result.scalar_one_or_none()

    async def edit_by_filter_async(self, filters: dict, data: dict):
        result = await self.session.execute(
            self.edit_by_filter_stmt(filters, data)
        )
        return result.scalars().all()

    async def get_all_async(self):
        result = await self.session.execute(self.get_all_stmt())
        return result.scalars().all()

    async def filter_by_async(self, one: bool = False, **filter_by):
        result = await self.session.execute(self.filter_by_stmt(**filter_by))
        return result.scalar_one_or_none() if one else result.scalars().all()

    async def filter_by_async_exists(self, **filter_by):
        result = await self.session.execute(
            select(exists(self.model)).filter_by(**filter_by)
        )
        return result.scalar()

    async def delete_async(self, **filter_by):
        await self.session.execute(self.delete_stmt(**filter_by))

    async def get_random_model_async(self, **filter_by):
        result = await self.session.execute(
            self.get_random_model_stmt(**filter_by)
        )
        return result.scalar_one_or_none()
