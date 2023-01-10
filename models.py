from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional

Base  = declarative_base()

class Loyalty_Plan(Base):
    __tablename__ = 'loyalty_plan'
    id = Column(Integer, primary_key=True, index=True)
    offer_limit = Column(Integer)
    if_premium = Column(Boolean,nullable=True) 
    subscription_plan = Column(String,nullable=True)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    comment_date = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = 'user'
    id  = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=True)
    surname = Column(String,nullable=True)
    email = Column(String)
    password = Column(String)
    nickname = Column(String)
    phone_num = Column(Integer,nullable=True)
    born_date = Column(Date,nullable=True)
    ad_amount = Column(Integer,nullable=True)
    comment_id = Column(Integer, ForeignKey('comment.id'),nullable=True)
    comment = relationship('Comment')
    



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
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    plant_id = Column(Integer, ForeignKey('plant.id'))
    plant = relationship('Plant')
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment = relationship('Comment')
    
    
   


