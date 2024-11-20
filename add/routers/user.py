from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert
from app.schemas import CreateCategory, CreateProduct

from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(Usr).where(User.is_active == True, User.stock > 0)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no user'
        )
    return users

@router.get('/{user_id}')
async def task_by_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    subcategories = db.scalars(select(User).where(User.parent_id == user.id)).all()
    users_and_subcategories = [user.id] + [i.id for i in subcategories]
    user_category = db.scalars(
        select(User).where(Product.user_id.in_(users_and_subcategories), User.is_active == True,
                              User.stock > 0)).all()
    return users_category


@router.post("/create")
async def create_user():
    pass
@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):
    db.execute(insert(Product).values(username=create_user.username,
                                      firstname=create_user.firstname,
                                      price=create_product.price,
                                      image_url=create_product.image_url,
                                      stock=create_product.stock,
                                      category_id=create_product.category,
                                      rating=0.0,
                                      slug=slugify(create_product.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
async def update_user():
    pass

@router.delete("/delete")
async def delete_user():
    pass
