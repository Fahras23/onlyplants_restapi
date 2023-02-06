from fastapi import FastAPI, HTTPException, Depends, status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import Users as ModelUser
from schema import AuthDetails
from auth import AuthHandler

import os
from dotenv import load_dotenv

from api import users,plans,offers,plants,comments

load_dotenv('.env')


app = FastAPI()
auth_handler = AuthHandler()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

#importing routers
app.include_router(users.router)
app.include_router(plans.router)
app.include_router(offers.router)
app.include_router(plants.router)
app.include_router(comments.router)


#login and register system
@app.post('/register', status_code=201)
def register(user: AuthDetails):
    user_exist = False

    hashed_password = auth_handler.get_password_hash(user.password)
    for user_in_database in db.session.query(ModelUser).all():
            if user_in_database.nickname == user.username:
                user_exist = True
                if user.username is not None:
                    user_in_database.nickname = user.username
                if user.password is not None:
                    user_in_database.password = hashed_password
                db.session.commit()
                break
               
    if user_exist==False:
        raise HTTPException(status_code=400, detail='user doesnt exist')

    return f"registered {user.username}"

@app.post('/login')
def login(user: AuthDetails):
    token_user = None
    for db_user in db.session.query(ModelUser).all():
        if db_user.nickname == user.username:
            token_user = db_user
            break
    
    if (token_user is None) or (not auth_handler.verify_password(user.password, token_user.password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(token_user.nickname)
    return { 'token': token }

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }

#menu endpoint
@app.get("/")
async def root():
    return {"rest-api": "onlyplants"}







