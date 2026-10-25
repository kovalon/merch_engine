from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from app.schemas.schemas import CategoryModel, CategoryRequestModel, CategoryListResponseModel
from app.services.categories import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_categories(
        category_service: Annotated[CategoryService, Depends()],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        parent_id: UUID | None = None
) -> list[CategoryListResponseModel]:
    return await category_service.get(db=db, parent_id=parent_id)

@router.get("/{id}")
async def get_category_by_id(
        category_service: Annotated[CategoryService, Depends()],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        id: UUID,
) -> CategoryModel:
    return await category_service.get_by_id(db=db, id=id)

@router.delete("/{id}")
async def delete_category_by_id(
        category_service: Annotated[CategoryService, Depends()],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        id: UUID,
) -> None:
    return await category_service.delete_by_id(db=db, id=id)

@router.post("")
async def create_category(
        category_service: Annotated[CategoryService, Depends()],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        category: CategoryRequestModel,
) -> CategoryModel:
    return await category_service.create(db=db, category=category)

@router.patch("/{id}")
async def update_category(
        category_service: Annotated[CategoryService, Depends()],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        id: UUID,
        category: CategoryRequestModel,
) -> CategoryModel:
    return await category_service.update(db=db, id=id, category=category)
