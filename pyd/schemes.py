from .base_models import *
from typing import List

class SchemeMovie(BaseMovie):
    genres: List[BaseGenre]
