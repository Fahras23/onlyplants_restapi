import fastapi
from fastapi import Depends, HTTPException
from auth import AuthHandler
from schema import Loyalty_Plan
from models import Users as ModelPlan
from fastapi_sqlalchemy import db

router = fastapi.APIRouter()
auth_handler = AuthHandler()

@router.get('/api/v1/plans')
async def plans(username=Depends(auth_handler.auth_wrapper)):
    items = db.session.query(ModelPlan).all()
    return items

@router.post('/api/v1/plans')
async def add_plan(plan:Loyalty_Plan,username=Depends(auth_handler.auth_wrapper)):
    db_plan = ModelPlan(
    id = plan.id,
    offer_limit = plan.offer_limit,
    subscription_plan = plan.subscription_plan,
    )
    db.session.add(db_plan)
    db.session.commit()
    return plan


@router.delete("/api/v1/plans/{item_id}")
async def delete_plan(item_id:int,username=Depends(auth_handler.auth_wrapper)):
    for item in db.session.query(ModelPlan).all():
        if item.id == item_id:
            db.session.delete(item)
            db.session.commit()
            return f"deleted user number {item_id}"
    raise HTTPException(
        status_code = 404,
        detail=f"{item} with id: {item_id} does not exists"
    )
