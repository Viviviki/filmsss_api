from pydantic import BaseModel, Field, EmailStr
from datetime import datetime as dt
from datetime import date
from typing import List

class CreateGenre(BaseModel):
    genre_name:str=Field(example='Триллер')
    genre_description:str|None=Field(example="Фильм-катастрофа")

class CreateMovie(BaseModel):
    movie_name:str=Field(example="Земля")
    year:int=Field(ge=1900, le=3000, example="2009")
    time:int=Field(gt=0, example=106)
    rate:float=Field(ge=0, le=10, example=6)
    description:str|None=Field(example="Фильм-катастрофа")
    poster:str=Field(example="/ссылка")
    add_date:date=Field(exmaple="2012-12-12")

    genres_id:List[int]=Field()

class CreateUser(BaseModel):
    username:str=Field(example="username", min_length=3, max_length=60)
    password:str=Field(example="password", min_length=8, max_length=20)
    email:EmailStr=Field(example="mail@mail.com")