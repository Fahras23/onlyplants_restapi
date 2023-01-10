import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import User, Offer, Plant, Loyalty_Plan, Comment

from models import User as ModelUser
from models import Offer as ModelOffer
from models import Plant as ModelPlant
from models import Loyalty_Plan as ModelPlan
from models import Comment as ModelComment

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])



@app.get("/")
async def root():
    return {"rest-api": "onlyplants"}

def get(item,model):
    @app.get(f'/api/v1/{item}s')
    async def items():
        items = db.session.query(model).all()
        return items

get("plan",ModelPlan)
get("comment",ModelComment)
get("user",ModelUser)
get("plant",ModelPlant)
get("offer",ModelOffer)

@app.post('/api/v1/plans')
async def add_plan(plan:Loyalty_Plan):
    db_plan = ModelPlan(
    id = plan.id,
    offer_limit = plan.offer_limit,
    subscription_plan = plan.subscription_plan,
    )
    db.session.add(db_plan)
    db.session.commit()
    return plan

@app.post('/api/v1/comments')
async def add_comment(comment: Comment):
    db_comment = ModelComment(
    id = comment.id,
    content = comment.content,
    )
    db.session.add(db_comment)
    db.session.commit()
    return comment

@app.post('/api/v1/users')
async def add_user(user:User):
    db_user = ModelUser(
    id = user.id,
    nickname = user.nickname,
    phone_num = user.phone_num,
    born_date = user.born_date,
    email = user.email,
    password = user.password
    )
    db.session.add(db_user)
    db.session.commit()
    return user 

@app.post('/api/v1/plants')
async def add_plant(plant:Plant):
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

@app.post('/api/v1/offers')
async def add_offer(offer:Offer):
    db_offer = ModelOffer(
    id = offer.id,
    user_id = offer.user_id,
    title = offer.title,
    description = offer.description,
    )
    db.session.add(db_offer)
    db.session.commit()
    return offer


def delete(item,model):
    @app.delete("/api/v1/"+item+"s/{item_id}")
    async def delete_user(item_id:int):
        for item in db.session.query(model).all():
            if item.id == item_id:
                db.session.delete(item)
                db.session.commit()
                return
        raise HTTPException(
            status_code = 404,
            detail=f"user with id: {item_id} does not exists"
    )

delete("plan",ModelPlan)
delete("comment",ModelComment)
delete("user",ModelUser)
delete("plant",ModelPlant)
delete("offer",ModelOffer)

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: User,user_id: int):
    for user in db.session.query(ModelUser).all():
        if user.id == user_id:
            if user_update.nickname is not None:
                user.nickname = user_update.nickname
            
            return user
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
  
# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)