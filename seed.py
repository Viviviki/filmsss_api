from datetime import datetime as dt
from sqlalchemy.orm import Session
from database import engine
import models as m
import bcrypt


m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    genre1 = m.Genre(
        genre_name = "Триллер"
    )
    session.add(genre1)

    genre2 = m.Genre(
        genre_name = "Боевик"
    )
    session.add(genre2)

    genre3 = m.Genre(
        genre_name = "Научная фантастика"
    )
    session.add(genre3)

    # Фильм 1
    movie1 = m.Movie(
        movie_name = "Знамение",
        duration = "106",
        rate = "6",
        genre_id = 1
    )
    session.add(movie1)

    # Фильм 2
    movie2 = m.Movie(
        movie_name = "Время",
        duration = "109",
        rate = "8.4",
        genre_id = 2
    )
    session.add(movie2)

    # Фильм 3
    movie3 = m.Movie(
        movie_name = "Довод",
        duration = "150",
        rate = "7.5",
        genre_id = 3
    )
    session.add(movie3)

    hall1 = m.Hall(

    )
    session.add(hall1)

    session1 = m.Session(
        movie_id = 1,
        hall_id = 1,
        time = dt.strptime("2011-10-27 02:20", "%Y-%m-%d %H:%M").date(), 
        price = 300
    )
    session.add(session1)

    user = m.User(
        login = "admin",
        first_name = "wiwiwi",
        last_name = "vivivi",
        password = bcrypt.hashpw(b"pass", bcrypt.gensalt()),
        email = "mail@mail.com"
    )
    session.add(user)

    place1 = m.Place(
        place_name = "Место"
    )
    session.add(place1)

    ticket1 = m.Ticket(
        session_id = 1,
        user_id = 1,
        place_id = 1
    )
    session.add(ticket1)


    session.commit()