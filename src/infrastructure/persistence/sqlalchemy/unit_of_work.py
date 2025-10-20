from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.unit_of_work import UnitOfWork

from .repositories import SQLAlchemyTodoRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.todos = SQLAlchemyTodoRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
