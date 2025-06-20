from datetime import date
from pydantic import BaseModel, Field, EmailStr

class BaseGenre(BaseModel):
    id:int=Field(example=1)
    genre_name:str=Field(example='Триллер')
    genre_description:str|None=Field(example="Фильм-катастрофа")

class BaseMovie(BaseModel):
    id:int=Field(example=1)
    movie_name:str=Field(example="Знамение")
    duration:int=Field(gt=0, example=106)
    rate:float=Field(ge=0, le=10, example=6)

class BaseSession(BaseModel):
    id:int=Field(example=1)
    hall_id:int=Field(example=1)
    time:date=Field(example="2017-12-01")
    price:float=Field(ge=0, example=6)

class BaseTicket(BaseModel):
    id:int=Field(example=1)

class BasePlace(BaseModel):
    id:int=Field(example=1)

class BaseRole(BaseModel):
    id:int=Field(example=1)
    role_name:str=Field(example="Зритель")
class BaseUser(BaseModel):
    id:int=Field(example=1)
    login:str=Field(exmaple="name")
    email:EmailStr=Field(example="mail@mail.com")

class BaseComment(BaseModel):
    id:int=Field(example=1)
    description:str=Field(exmaple="Отзыв о фильме")
