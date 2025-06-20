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
import logging
from datetime import datetime as dt
from auth import auth_handler

logging.basicConfig(level=logging.INFO, filename="logs.log",filemode="w")

app=FastAPI()


# Вход
@app.post("/login")
def user_auth(login: pyd.LoginUser, db: Session=Depends(get_db)):
    user_db = db.query(m.User).filter(
        m.User.login == login.login
    ).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден!")
    if auth_handler.verify_password(login.password, user_db.password):
        # logging.info(f"{dt.now()} - User: {user_db.username} loggined")
        return {"token": auth_handler.encode_token(user_db.id, user_db.role_id)}
    # logging.info(f"{dt.now()} - User: {user_db.username} fail authentication")
    raise HTTPException(400, "Доступ запрещён!")

@app.get("/api/movies", response_model=List[pyd.SchemeMovie])
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

@app.get("/api/movie/{id}", response_model=pyd.SchemeMovie)
def get_movie(id:int, db:Session=Depends(get_db)):
    movie = db.query(m.Movie).filter(m.Movie.id==id).first()
    if not movie:
        raise HTTPException(404, "Фильм не найден")
    return movie

@app.post("/api/movie/", response_model=pyd.SchemeMovie)
def create_movie(movie:pyd.CreateMovie, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.admin_wrapper)):
    movie_db =m.Movie()
    movie_db.movie_name = movie.movie_name
    movie_db.duration = movie.duration
    movie_db.rate = movie.rate
    genre_db = db.query(m.Genre).filter(m.Genre.id==movie.genre_id).first()
    if not genre_db:
        raise HTTPException(404, "Жанр не найден")
    movie_db.genre_id = movie.genre_id
    db.add(movie_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} added movie: {movie_db.id}")
    return movie_db

@app.put("/api/movie/{id}", response_model=pyd.SchemeMovie)
def edit_movie(id:int, movie:pyd.CreateMovie, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.admin_wrapper)):
    movie_db = db.query(m.Movie).filter(m.Movie.id==id).first()
    if not movie_db:
        raise HTTPException(404, "Фильм не найден")
    movie_db.movie_name = movie.movie_name
    movie_db.duration = movie.duration
    movie_db.rate = movie.rate
    genre_db = db.query(m.Genre).filter(m.Genre.id==movie.genre_id).first()
    if not genre_db:
        raise HTTPException(404, "Жанр не найден")
    movie_db.genre_id = movie.genre_id
    db.add(movie_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} edit movie: {movie_db.id}")
    return movie_db

@app.delete("/api/movie/{id}")
def delete_movie(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.admin_wrapper)):
    movie = db.query(m.Movie).filter(m.Movie.id==id).first()
    if not movie:
        raise HTTPException(404, "Фильм не найден")
    db.delete(movie)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} delete movie: {movie.id}")
    return {"detail":"Фильм удален"}

@app.get("/api/sessions", response_model=List[pyd.SchemeSession])
def get_sessions(db:Session=Depends(get_db)):
    sessions = db.query(m.Session).all()
    if not sessions:
        raise HTTPException(404, "Сеансы не найдены")
    return sessions

@app.get("/api/session/{id}", response_model=pyd.SchemeSession)
def get_session(id:int, db:Session=Depends(get_db)):
    session = db.query(m.Session).filter(m.Session.id==id).first()
    if not session:
        raise HTTPException(404, "Сеанс не найден")
    return session

@app.post("/api/session/", response_model=pyd.SchemeSession)
def create_session(session:pyd.CreateSession, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.seller_wrapper)):
    session_db =m.Session()
    movie_db = db.query(m.Movie).filter(m.Movie.id==session.movie_id).first()
    if not movie_db:
        raise HTTPException(404, "Фильм не найден")
    session_db.movie_id = session.movie_id
    hall_db = db.query(m.Hall).filter(m.Hall.id==session.hall_id).first()
    if not hall_db:
        raise HTTPException(404, "Зал не найден")
    session_db.hall_id = session.hall_id
    session_db.time = session.time
    session_db.price = session.price
    db.add(session_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} added session: {session_db.id}")
    return session_db

@app.put("/api/session/{id}", response_model=pyd.SchemeSession)
def edit_session(id:int, session:pyd.CreateSession, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.seller_wrapper)):
    session_db = db.query(m.Session).filter(m.Session.id==id).first()
    if not session_db:
        raise HTTPException(404, "Сеанс не найден")
    movie_db = db.query(m.Movie).filter(m.Movie.id==session.movie_id).first()
    if not movie_db:
        raise HTTPException(404, "Фильм не найден")
    session_db.movie_id = session.movie_id
    hall_db = db.query(m.Hall).filter(m.Hall.id==session.hall_id).first()
    if not hall_db:
        raise HTTPException(404, "Зал не найден")
    session_db.hall_id = session.hall_id
    session_db.time = session.time
    session_db.price = session.price
    db.add(session_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} edit session: {session_db.id}")
    return session_db

@app.delete("/api/session/{id}")
def delete_session(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.seller_wrapper)):
    session = db.query(m.Session).filter(m.Session.id==id).first()
    if not session:
        raise HTTPException(404, "Сеанс не найден")
    db.delete(session)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} delete session: {session.id}")
    return {"detail":"Сеанс удален"}

@app.get("/api/tickets", response_model=List[pyd.SchemeTicket])
def get_tickets(db:Session=Depends(get_db)):
    tickets = db.query(m.Ticket).all()
    if not tickets:
        raise HTTPException(404, "Билеты не найдены")
    return tickets

@app.get("/api/tickets/{id}", response_model=pyd.SchemeTicket)
def get_ticket(id:int, db:Session=Depends(get_db)):
    ticket = db.query(m.Ticket).filter(m.Ticket.id==id).first()
    if not ticket:
        raise HTTPException(404, "Билет не найден")
    return ticket

@app.post("/api/ticket/", response_model=pyd.SchemeTicket)
def create_ticket(ticket:pyd.CreateTicket, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    ticket_db =m.Ticket()
    session_db = db.query(m.Session).filter(m.Session.id==ticket.session_id).first()
    if not session_db:
        raise HTTPException(404, "Сеанс не найден")
    ticket_db.session_id = ticket.session_id
    user_db = db.query(m.User).filter(m.User.id==ticket.user_id).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    ticket_db.user_id = ticket.user_id
    place_db = db.query(m.Place).filter(m.Place.id==ticket.place_id).first()
    if not place_db:
        raise HTTPException(404, "Место не найдено")
    ticket_db.place_id = ticket.place_id
    db.add(ticket_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} create ticket: {ticket_db.id}")
    return ticket_db

@app.put("/api/ticket/{id}", response_model=pyd.SchemeTicket)
def edit_ticket(id:int, ticket:pyd.CreateTicket, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.seller_wrapper)):
    ticket_db = db.query(m.Ticket).filter(m.Ticket.id==id).first()
    if not ticket_db:
        raise HTTPException(404, "Билет не найден")
    session_db = db.query(m.Session).filter(m.Session.id==ticket.session_id).first()
    if not session_db:
        raise HTTPException(404, "Сеанс не найден")
    ticket_db.session_id = ticket.session_id
    user_db = db.query(m.User).filter(m.User.id==ticket.user_id).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    ticket_db.user_id = ticket.user_id
    place_db = db.query(m.Place).filter(m.Place.id==ticket.place_id).first()
    if not place_db:
        raise HTTPException(404, "Место не найдено")
    ticket_db.place_id = ticket.place_id
    db.add(ticket_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} edit ticket: {ticket_db.id}")
    return ticket_db

@app.delete("/api/ticket/{id}")
def delete_ticket(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.seller_wrapper)):
    ticket = db.query(m.Ticket).filter(m.Ticket.id==id).first()
    if not ticket:
        raise HTTPException(404, "Билет не найден")
    db.delete(ticket)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} delete ticket: {ticket.id}")
    return {"detail":"Билет удален"}

@app.get("/api/comments", response_model=List[pyd.SchemeComment])
def get_comments(db:Session=Depends(get_db)):
    comments = db.query(m.Comment).all()
    if not comments:
        raise HTTPException(404, "Отзывы не найдены")
    return comments

@app.get("/api/comments/{id}", response_model=pyd.SchemeComment)
def get_comment(id:int, db:Session=Depends(get_db)):
    comment = db.query(m.Comment).filter(m.Comment.id==id).first()
    if not comment:
        raise HTTPException(404, "Отзыв не найден")
    return comment

@app.post("/api/comment/", response_model=pyd.SchemeComment)
def create_comment(comment:pyd.CreateComment, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    comment_db =m.Comment()
    movie_db = db.query(m.Movie).filter(m.Movie.id==comment.movie_id).first()
    if not movie_db:
        raise HTTPException(404, "Фильм не найден")
    comment_db.movie_id = comment.movie_id
    user_db = db.query(m.User).filter(m.User.id==comment.user_id).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    comment_db.user_id = comment.user_id
    if comment.user_id != user["user_id"]:
        logging.info(f"{dt.now()} - User {user['user_id']} tried to create a comment on behalf of the user {comment.user_id}")
        raise HTTPException(403, "Please be honest and write a comment on your own behalf.")
    comment_db = m.Comment()
    comment_db.description = comment.description
    db.add(comment_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} created a comment: {comment_db.id}")
    return comment_db

@app.put("/api/comment/{id}", response_model=pyd.SchemeTicket)
def edit_comment(id:int, comment:pyd.CreateComment, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    comment_db = db.query(m.Comment).filter(m.Comment.id==id).first()
    if not comment_db:
        raise HTTPException(404, "Отзыв не найден")
    movie_db = db.query(m.Movie).filter(m.Movie.id==comment.movie_id).first()
    if not movie_db:
        raise HTTPException(404, "Фильм не найден")
    comment_db.movie_id = comment.movie_id
    if comment.user_id != user["user_id"]:
        logging.info(f"{dt.now()} - User {user['user_id']} tried to change the user's comment {comment.user_id}")
        raise HTTPException(403, "You can't change a comment that someone else wrote.")
    comment_db = m.Comment()
    comment_db.description = comment.description
    db.add(comment_db)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} edit comment: {comment_db.id}")
    return comment_db

@app.delete("/api/comment/{id}")
def delete_comment(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    comment = db.query(m.Comment).filter(m.Comment.id==id).first()
    if not comment:
        raise HTTPException(404, "Отзыв не найден")
    if comment.user_id != user["user_id"]:
        logging.info(f"{dt.now()} - User {user['user_id']} tried to delete the user's comment {comment.user_id}")
        raise HTTPException(403, "You cannot delete a comment that was written by someone else")
    db.delete(comment)
    db.commit()
    logging.info(f"{dt.now()} - User: {user["user_id"]} delete comment: {comment.id}")
    return {"detail":"Отзыв удален"}

