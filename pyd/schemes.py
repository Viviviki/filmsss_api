from .base_models import *

class SchemeMovie(BaseMovie):
    genre: BaseGenre

class SchemeSession(BaseSession):
    movie: SchemeMovie

class SchemeUser(BaseUser):
    role: BaseRole

class SchemeTicket(BaseTicket):
    session : SchemeSession
    user: BaseUser
    place: BasePlace