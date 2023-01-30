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
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return

@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
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
async def add_comment(comment: Comment):
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
    async def delete_user(item_id:int,username=Depends(auth_handler.auth_wrapper)):
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
            if user_update.phone_num is not None:
                user.phone_num = user_update.phone_num
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.password is not None:
                user.password = user_update.password
            db.session.commit()
            return user
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: User,user_id: int):
    for user in db.session.query(ModelUser).all():
        if user.id == user_id:
            if user_update.nickname and user_update.password:
                user = user_update
                db.session.commit()

    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

@app.put("/api/v1/comments/{comment_id}")
async def update_user(comment_update: Comment,comment_id: int):
    for comment in db.session.query(ModelComment).all():
        if comment.id == comment_id:
            if comment_update.content:
                comment = comment_update
                db.session.commit()
                
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {comment_id} does not exists"
    )

