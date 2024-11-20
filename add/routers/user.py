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
    user_task = db.scalars(
        select(User).where(User.user_id.in_(users_and_subtasks), User.is_active == True,
                              User.stock > 0)).all()
    return users_task

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(id=create_user.id,
                                      username=create_user.username,
                                      firstname=create_user.firstname,
                                      age=create_user.age,
                                      lastname=create_user.lastname,
                                      slug=slugify(create_user.name
                                      )))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_slug: str,
                         update_user_model: CreateUser):
    user_update = db.scalar(select(User).where(User.slug == user_slug))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )

    db.execute(update(User).where(User.slug == user_slug)
               .values(id=create_user.id,
                        username=create_user.username,
                        firstname=create_user.firstname,
                        age=create_user.age,
                        lastname=create_user.lastname,
                        slug=slugify(create_user.name)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }

@router.delete("/delete")
async def delete_user():
    pass
@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_delete = db.scalar(select(User).where(User.id == product_id))
    if user_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )
    db.execute(update(User).where(User.id == user_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }
