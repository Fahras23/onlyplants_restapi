import fastapi
from fastapi import Depends, HTTPException
from auth import AuthHandler
from schema import Offer
from models import Users as ModelOffer
from fastapi_sqlalchemy import db

router = fastapi.APIRouter()
auth_handler = AuthHandler()

@router.get('/api/v1/offers')
async def offers(username=Depends(auth_handler.auth_wrapper)):
    items = db.session.query(ModelOffer).all()
    return items

@router.post('/api/v1/offers')
async def add_offer(offer:Offer,username=Depends(auth_handler.auth_wrapper)):
    db_offer = ModelOffer(
    id = offer.id,
    user_id = offer.user_id,
    title = offer.title,
    description = offer.description,
    )
    db.session.add(db_offer)
    db.session.commit()
    return offer
    
@router.delete("/api/v1/offers/{item_id}")
async def delete_offer(item_id:int,username=Depends(auth_handler.auth_wrapper)):
    for item in db.session.query(ModelOffer).all():
        if item.id == item_id:
            db.session.delete(item)
            db.session.commit()
            return f"deleted user number {item_id}"
    raise HTTPException(
        status_code = 404,
        detail=f"{item} with id: {item_id} does not exists"
    )

@router.put("/api/v1/offers/{offer_id}")
async def update_offer(offer_update: Offer,offer_id: int,username=Depends(auth_handler.auth_wrapper)):
    for offer in db.session.query(ModelOffer).all():
        if offer.id == offer_id:
            if offer_update.title is not None:
                offer.title = offer_update.title
            db.session.commit()
            return offer
    raise HTTPException(
        status_code=404,
        detail=f"offer with id: {offer_id} does not exists"
    )
