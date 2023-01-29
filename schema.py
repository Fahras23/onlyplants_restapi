# build a schema using pydantic
from typing import List
from pydantic import BaseModel
from datetime import date



class AuthDetails(BaseModel):
    username: str
    password: str
    
class Roles(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class Loyalty_Plan(BaseModel):
    id: int
    offer_limit: int
    subscription_plan: str
    
    class Config:
        orm_mode = True

class Comment(BaseModel):
    id: int
    content: str
 
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    nickname: str
    surname: str
    name: str
    phone_num: int
    born_date: date
    email: str
    password: str
    ad_amount: int
    loyalty_plan_id: int
    roles_id: int   

    class Config:
        orm_mode = True

class Plant(BaseModel):
    id: int
    type: str
    plant_name: str
    international_name: str
    pot_diameter: int
    special_features: str
    class Config:
        orm_mode = True

class Offer(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    class Config:
        orm_mode = True

