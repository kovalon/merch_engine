from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import ValidationException, NotFoundException
from app.exceptions.schemas import DetailModel, DetailType
from app.models.categories import CategoryTable
from app.repositories.categories import category_repository
from app.schemas.converters import category_table_to_category_model
from app.schemas.schemas import CategoryModel, CategoryRequestModel, CategoryListResponseModel


class CategoryService:

    def __init__(self):
        self.category_repository = category_repository

    async def get(self, db: AsyncSession, parent_id: UUID | None) -> list[CategoryListResponseModel]:
        categories = await self.category_repository.get(db=db, parent_id=parent_id)
        return [
            CategoryListResponseModel.model_validate(category) for category in categories
        ]

    async def create(self, db: AsyncSession, category: CategoryRequestModel) -> CategoryModel:
        db_category = CategoryTable(**category.model_dump())
        if category.parent_id:
            parent_category = await self.category_repository.get_by_id(db=db, id=category.parent_id)
            if not parent_category:
                raise ValidationException(details=[DetailModel(name="parent_id", error=DetailType.NOT_FOUND)])
            db_category.path = parent_category.path.copy()
            db_category.path.append(parent_category.id)
        db_result = await self.category_repository.create(session=db, data=db_category)
        return CategoryModel.model_validate(db_result)

    # Пределать update
    async def update(self, db: AsyncSession, id: UUID, category: CategoryRequestModel) -> CategoryModel:
        updating_category = await self.category_repository.get_by_id(db=db, id=id)
        if not updating_category:
            raise NotFoundException
        updating_category.name = category.name if category.name else updating_category.name
        if category.parent_id:
            parent_category = await self.category_repository.get_by_id(db=db, id=category.parent_id)
            if not parent_category:
                raise ValidationException(details=[DetailModel(name="parent_id", error=DetailType.NOT_FOUND)])
            updating_category.path = parent_category.path if parent_category.path else []
            updating_category.path.append(parent_category.id)
            updating_category.parent_id = category.parent_id
        db_result = await self.category_repository.update(session=db, data=updating_category)
        return CategoryModel.model_validate(db_result)

    async def get_by_id(self, db: AsyncSession, id: UUID) -> CategoryModel:
        db_result = await self.category_repository.get_by_id(db=db, id=id)
        if not db_result:
            raise NotFoundException
        return category_table_to_category_model(db_result)

    async def delete_by_id(self, db: AsyncSession, id: UUID) -> None:
        await self.category_repository.delete(session=db, id=id)
