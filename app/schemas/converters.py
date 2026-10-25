from app.models.categories import CategoryTable
from app.schemas.schemas import CategoryModel


def category_table_to_category_model(category: CategoryTable) -> CategoryModel:
    return CategoryModel(
        id=category.id,
        name=category.name,
        parent_id=category.parent_id,
        path=category.path,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )

