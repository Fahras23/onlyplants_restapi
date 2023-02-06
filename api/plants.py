import fastapi
from fastapi import Depends, HTTPException
from auth import AuthHandler
from schema import Plant
from models import Users as ModelPlant
from fastapi_sqlalchemy import db

router = fastapi.APIRouter()
auth_handler = AuthHandler()

@router.get('/api/v1/plants')
async def plants(username=Depends(auth_handler.auth_wrapper)):
    items = db.session.query(ModelPlant).all()
    return items

@router.post('/api/v1/plants')
async def add_plant(plant:Plant,username=Depends(auth_handler.auth_wrapper)):
    db_plant = ModelPlant(
    id = plant.id,
    type = plant.type,
    international_name = plant.international_name,
    pot_diameter = plant.pot_diameter,
    special_features = plant.special_features
    )
    db.session.add(db_plant)
    db.session.commit()
    return plant

@router.delete("/api/v1/plants/{item_id}")
async def delete_plant(item_id:int,username=Depends(auth_handler.auth_wrapper)):
    for item in db.session.query(ModelPlant).all():
        if item.id == item_id:
            db.session.delete(item)
            db.session.commit()
            return f"deleted user number {item_id}"
    raise HTTPException(
        status_code = 404,
        detail=f"{item} with id: {item_id} does not exists"
    )