from pydantic import BaseModel
from typing import Optional, List

from model.pesquisa import Pesquisa

class ErrorSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    mesage: str
