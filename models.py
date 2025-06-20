from database import Base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Genre(Base):
    __tablename__="genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(20), unique=True)
    genre_description = Column(String(255), nullable=True)

class Movie(Base):
    __tablename__="movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(255))
    duration = Column(Integer)
    rate = Column(Float)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    
    genre = relationship("Genre", backref="movies")

class Session(Base):
    __tablename__="sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    time = Column(DateTime)
    price = Column(Float)

    movie = relationship("Movie", backref="sessions")

class Ticket(Base):
    __tablename__="tickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))

    session = relationship("Session", backref="tickets")
    user = relationship("User", backref="tickets")
    place = relationship("Place", backref="tickets")

class Hall(Base):
    __tablename__="halls"
    id = Column(Integer, primary_key=True, autoincrement=True)

class Place(Base):
    __tablename__="places"
    id = Column(Integer, primary_key=True, autoincrement=True)
    place_name = Column(String)

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)

    role = relationship("Role", backref='users')

class Role(Base):
    __tablename__="roles"
    id=Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(20), unique=True)