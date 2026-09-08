from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from auth import get_current_admin
from models import Category, User
from schema import (
    CategoryCreate,
    UpdateCategory,
    CategoryResponse,
    CategoryWithProductsResponse
)


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post(
    "",
    response_model=CategoryResponse
)
def create_category(
    data: CategoryCreate,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    new_category = Category(
        name=data.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def list_categories(
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Category)
    )

    categories = result.scalars().all()

    return categories


@router.get(
    "/{category_id}",
    response_model=CategoryWithProductsResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Category).where(
            Category.id == category_id
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )

    return category


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    data: UpdateCategory,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Category).where(
            Category.id == category_id
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )

    category.name = data.name

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Category).where(
            Category.id == category_id
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )

    if category.products:
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir uma categoria que possui produtos."
        )

    db.delete(category)
    db.commit()

    return "Categoria excluída com sucesso."
