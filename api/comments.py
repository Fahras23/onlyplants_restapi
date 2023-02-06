import fastapi
from fastapi import Depends, HTTPException
from auth import AuthHandler
from schema import Comment
from models import Users as ModelComment
from fastapi_sqlalchemy import db

router = fastapi.APIRouter()
auth_handler = AuthHandler()

@router.get('/api/v1/comments')
async def comments(username=Depends(auth_handler.auth_wrapper)):
    items = db.session.query(ModelComment).all()
    return items

@router.post('/api/v1/comments')
async def add_comment(comment: Comment,username=Depends(auth_handler.auth_wrapper)):
    db_comment = ModelComment(
    id = comment.id,
    content = comment.content,
    )
    db.session.add(db_comment)
    db.session.commit()
    return comment

@router.delete("/api/v1/comments/{item_id}")
async def delete_comment(item_id:int,username=Depends(auth_handler.auth_wrapper)):
    for item in db.session.query(ModelComment).all():
        if item.id == item_id:
            db.session.delete(item)
            db.session.commit()
            return f"deleted user number {item_id}"
    raise HTTPException(
        status_code = 404,
        detail=f"{item} with id: {item_id} does not exists"
    )