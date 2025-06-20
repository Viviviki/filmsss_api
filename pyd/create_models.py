from pydantic import BaseModel, Field, EmailStr
from datetime import datetime as dt
from datetime import date
from typing import List
import re

class CreateGenre(BaseModel):
    genre_name:str=Field(example='Триллер')
    genre_description:str|None=Field(example="Фильм-катастрофа")

class CreateMovie(BaseModel):
    movie_name:str=Field(example="Знамение")
    duration:int=Field(gt=0, example=106)
    rate:float=Field(ge=0, le=10, example=6)
    genre_id:int=Field(example=1)

class CreateSession(BaseModel):
    movie_id:int=Field(example=1)
    hall_id:int=Field(example=1)
    time:date=Field(example="2017-12-01")
    price:float=Field(ge=0, example=6)

class CreateTicket(BaseModel):
    session_id:int=Field(example=1)
    user_id:int=Field(example=1)
    place_id:int=Field(example=1)
    
class CreateComment(BaseModel):
    description:str=Field(exmaple="Отзыв о фильме")
    movie_id:int=Field(example=1)
    user_id:int=Field(example=1)

class LoginUser(BaseModel):
    login:str=Field(example="1v4n", min_length=2, max_length=20)
    password:str=Field(example="1v4n", min_length=8, max_length=20, pattern=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"))