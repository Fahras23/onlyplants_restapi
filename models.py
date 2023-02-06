from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional

Base  = declarative_base()
class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=True)

class Loyalty_Plan(Base):
    __tablename__ = 'loyalty_plan'
    id = Column(Integer, primary_key=True, index=True)
    offer_limit = Column(Integer)
    if_premium = Column(Boolean,nullable=True) 
    subscription_plan = Column(Boolean,nullable=True) 

#users not user because user is taken by postgres
class Users(Base):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=True)
    surname = Column(String,nullable=True)
    email = Column(String)
    password = Column(String)
    nickname = Column(String)
    phone_num = Column(Integer,nullable=True)
    born_date = Column(Date,nullable=True)
    ad_amount = Column(Integer,nullable=True)
    loyalty_plan_id = Column(Integer, ForeignKey('loyalty_plan.id'),nullable=True)
    loyalty_plan = relationship('Loyalty_Plan')    
    roles_id = Column(Integer, ForeignKey('roles.id'),nullable=True)
    roles = relationship('Roles')   
    
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    comment_date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'),nullable=True)
    user = relationship('Users')    
    offer_id = Column(Integer, ForeignKey('offer.id'),nullable=True)
    offer = relationship('Offer')    

class Plant(Base):
    __tablename__ = 'plant'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    plant_name = Column(String)
    international_name = Column(String,nullable=True) 
    pot_diameter = Column(Integer,nullable=True)
    special_features = Column(String,nullable=True) 

class Offer(Base):
    __tablename__ = 'offer'
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String,nullable=True)
    plant_condition = Column(String,nullable=True) 
    photo = Column(String,nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    if_premium = Column(Boolean,nullable=True) 
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users')
    plant_id = Column(Integer, ForeignKey('plant.id'))
    plant = relationship('Plant')
   
    
   


