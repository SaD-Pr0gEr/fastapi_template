from abc import ABC, abstractmethod

from sqlalchemy import Select, func, Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class BasePaginator(ABC):
    @abstractmethod
    def pages_count_calc(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_next_page(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_prev_page(self, *args, **kwargs):
        pass

    @abstractmethod
    def paginate(self, *args, **kwargs):
        pass


class BasePagePaginator(BasePaginator, ABC):
    def __init__(
            self, page_per_count: int | None = 10, current_page: int | None = 1
    ) -> None:
        self.page_per_count = page_per_count or 10
        self.current_page = current_page or 1

    @abstractmethod
    def pages_count(self, *args, **kwargs):
        pass

    @abstractmethod
    def paginate_stmt(self, *args, **kwargs):
        pass

    @classmethod
    def get_stmt_db_class(cls, stmt: Select):
        return stmt.column_descriptions[0]['entity']

    def pages_count_stmt(self, stmt: Select):
        db_class = self.get_stmt_db_class(stmt)
        return select(func.count()).select_from(db_class)

    def get_offset(self, db_pages_count: int) -> int:
        if self.current_page > db_pages_count:
            self.current_page = db_pages_count
        elif self.current_page < 1:
            self.current_page = 1
        offset = (self.current_page - 1) * self.page_per_count
        return offset

    def pages_count_calc(self, count: int):
        return count // self.page_per_count + bool(count % self.page_per_count)

    def has_next_page(self, pages_count: int) -> bool:
        return 1 <= self.current_page + 1 <= pages_count

    def has_prev_page(self, pages_count: int) -> bool:
        return 1 <= self.current_page - 1 <= pages_count

    def next_page(self, session: Session | AsyncSession, stmt: Select) -> bool:
        return self.has_next_page(self.pages_count(session, stmt))

    def prev_page(self, session: Session | AsyncSession, stmt: Select) -> bool:
        return self.has_prev_page(self.pages_count(session, stmt))


class PagePaginator(BasePagePaginator):

    def pages_count(self, session: Session, stmt: Select) -> int:
        stmt = self.pages_count_stmt(stmt)
        count = session.execute(stmt).scalar() or 1
        return self.pages_count_calc(count)

    def paginate(self, session: Session, stmt: Select) -> Sequence:
        stmt = self.paginate_stmt(session, stmt)
        return session.execute(stmt).scalars().all()

    def paginate_stmt(
            self, session: Session, stmt: Select
    ) -> Select:
        return stmt.offset(
            self.get_offset(self.pages_count(session, stmt))
        ).limit(self.page_per_count)


class AsyncPagePaginator(BasePagePaginator):

    async def pages_count(self, session: AsyncSession, stmt: Select) -> int:
        stmt = self.pages_count_stmt(stmt)
        count = (await session.execute(stmt)).scalar() or 1
        return self.pages_count_calc(count)

    async def paginate(self, session: AsyncSession, stmt: Select,
                       unique: bool = False) -> Sequence:
        stmt = await self.paginate_stmt(session, stmt)
        result = await session.execute(stmt)
        if unique:
            return result.unique().scalars().all()
        return result.scalars().all()

    async def paginate_stmt(
            self, session: AsyncSession, stmt: Select
    ) -> Select:
        return stmt.offset(
            self.get_offset(await self.pages_count(session, stmt))
        ).limit(self.page_per_count)
