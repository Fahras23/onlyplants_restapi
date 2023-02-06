import fastapi
from fastapi import Depends, HTTPException
from auth import AuthHandler
from schema import User
from models import Users as ModelUser
from fastapi_sqlalchemy import db

router = fastapi.APIRouter()
auth_handler = AuthHandler()


@router.get('/api/v1/users')
async def users(username=Depends(auth_handler.auth_wrapper)):
    items = db.session.query(ModelUser).all()
    return items

@router.post('/api/v1/users')
async def add_user(user:User,username=Depends(auth_handler.auth_wrapper)):
    db_user = ModelUser(
    id = user.id,
    name = user.name,
    surname = user.surname,
    nickname = user.nickname,
    phone_num = user.phone_num,
    born_date = user.born_date,
    email = user.email,
    password = user.password,
    ad_amount =  user.ad_amount,
    loyalty_plan_id = user.loyalty_plan_id,
    roles_id = user.roles_id
    )
    db.session.add(db_user)
    db.session.commit()
    return user 


@router.delete("/api/v1/users/{item_id}")
async def delete_user(item_id:int,username=Depends(auth_handler.auth_wrapper)):
    for item in db.session.query(ModelUser).all():
        if item.id == item_id:
            db.session.delete(item)
            db.session.commit()
            return f"deleted user number {item_id}"
    raise HTTPException(
        status_code = 404,
        detail=f"{item} with id: {item_id} does not exists"
    )

@router.put("/api/v1/users/{user_id}")
async def update_user(user_update: User,user_id: int,username=Depends(auth_handler.auth_wrapper)):
    for user in db.session.query(ModelUser).all():
        if user.id == user_id:
            if user_update.nickname is not None:
                user.nickname = user_update.nickname
            if user_update.password is not None:
                user.password = user_update.password
            db.session.commit()
            return user
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

