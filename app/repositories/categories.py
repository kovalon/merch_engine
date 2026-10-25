from uuid import UUID
from sqlalchemy import select, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categories import CategoryTable


class CategoryRepository:
    def __init__(self):
        pass

    async def get(self, db: AsyncSession, parent_id: UUID | None) -> Sequence[CategoryTable]:
        query = select(CategoryTable).where(CategoryTable.parent_id == parent_id)
        result = await db.execute(query)
        return result.scalars().all()


    async def get_by_id(self, db: AsyncSession, id: UUID) -> CategoryTable:
        result = await db.execute(select(CategoryTable).filter(CategoryTable.id == id))
        return result.scalars().first()

    async def create(self, session: AsyncSession, data: CategoryTable) -> CategoryTable:
        session.add(data)
        await session.commit()
        return data

    async def update(self, session: AsyncSession, data: CategoryTable) -> CategoryTable:
        session.add(data)
        await session.commit()
        await session.refresh(data, ["updated_at"])
        return data

    async def delete(self, session: AsyncSession, id: UUID) -> None:
        await session.execute(delete(CategoryTable).filter(CategoryTable.id == id))


category_repository = CategoryRepository()

