import os
import shutil
from fastapi import FastAPI, HTTPException, Depends, UploadFile, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
import string
import random
import bcrypt


app=FastAPI()

@app.get("/api/movies")
def get_movies(page:int=Query(1, gt=0), limit:int|None=Query(None, gt=0, le=100), genre:str|None=Query(None), minRating:float|None=Query(None, ge=0), db:Session=Depends(get_db)):
    movies = db.query(m.Movie)
    if genre:
        genre_db = db.query(m.Genre).filter(
            m.Genre.genre_name == genre
        ).first()
        if not genre_db:
            raise HTTPException(404, "Жанры не найдены")
        movies = movies.filter(
            m.Movie.genre_id == genre_db.id
        )
    if minRating:
        movies = movies.filter(
            m.Movie.rate >= minRating
        )
    if limit:
        movies = movies[(page - 1) * limit:page * limit]
        if not movies:
            raise HTTPException(404, "Фильмы не найдены")
        return movies
    all_movies = movies.all()
    if not all_movies:
        raise HTTPException(404, "Фильмы не найдены")
    return all_movies