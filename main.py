from fastapi import FastAPI, HTTPException, Depends, status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from schema import User, Offer, Plant, Loyalty_Plan, Comment, AuthDetails

from models import Users as ModelUser
from models import Offer as ModelOffer
from models import Plant as ModelPlant
from models import Loyalty_Plan as ModelPlan
from models import Comment as ModelComment

from auth import AuthHandler

import os
from dotenv import load_dotenv


load_dotenv('.env')


app = FastAPI()
users = []
auth_handler = AuthHandler()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

#login and register system
@app.post('/register', status_code=201)
def register(user: AuthDetails):
    user_exist = None
    #if any(x['username'] == auth_details.username for x in users):
        #raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(user.password)
    for user_in_database in db.session.query(ModelUser).all():
            if user_in_database.nickname == user.username:
                user_exist = True
                if user.username is not None:
                    user_in_database.nickname = user.username
                if user.password is not None:
                    user_in_database.password = user.password
                db.session.commit()

    return f"registered {user}"

@app.post('/login')
def login(user: AuthDetails):
    #user = None
    db_user = None
    for db_user in db.session.query(ModelUser).all():
        if db_user == user.username:
            user = db_user
            db_user = db_user
            break
    
    if (user is None) or (not auth_handler.verify_password(user.password, db_user.password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user.username)
    return { 'token': token }

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }

#routing endpoints
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
async def add_plan(plan:Loyalty_Plan,username=Depends(auth_handler.auth_wrapper)):
    db_plan = ModelPlan(
    id = plan.id,
    offer_limit = plan.offer_limit,
    subscription_plan = plan.subscription_plan,
    )
    db.session.add(db_plan)
    db.session.commit()
    return plan

@app.post('/api/v1/comments')
async def add_comment(comment: Comment,username=Depends(auth_handler.auth_wrapper)):
    db_comment = ModelComment(
    id = comment.id,
    content = comment.content,
    )
    db.session.add(db_comment)
    db.session.commit()
    return comment

@app.post('/api/v1/users')
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

@app.post('/api/v1/plants')
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

@app.post('/api/v1/offers')
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


def delete(item,model):
    @app.delete("/api/v1/"+item+"s/{item_id}")
    async def delete_user(item_id:int,username=Depends(auth_handler.auth_wrapper)):
        for item in db.session.query(model).all():
            if item.id == item_id:
                db.session.delete(item)
                db.session.commit()
                return
        raise HTTPException(
            status_code = 404,
            detail=f"{item} with id: {item_id} does not exists"
    )

delete("plan",ModelPlan)
delete("comment",ModelComment)
delete("user",ModelUser)
delete("plant",ModelPlant)
delete("offer",ModelOffer)

@app.put("/api/v1/users/{user_id}")
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

@app.put("/api/v1/comments/{comment_id}")
async def update_comment(comment_update: Comment,comment_id: int,username=Depends(auth_handler.auth_wrapper)):
    for comment in db.session.query(ModelComment).all():
        if comment.id == comment_id:
            if comment_update.content is not None:
                comment.content = comment_update.content
            db.session.commit()
            return comment
    raise HTTPException(
        status_code=404,
        detail=f"comment with id: {comment_id} does not exists"
    )
@app.put("/api/v1/offers/{offer_id}")
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
