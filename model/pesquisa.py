from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from model import Base

class Pesquisa(Base):
    __tablename__ = 'pesquisa'

    id = Column("pk_pesquisa", Integer, primary_key = True)
    nome = Column(String(130), unique = True)
    idade = Column(Integer, unique = False)
    time = Column(String(130), unique = False)

    def __init__(self, nome:str, idade: int, time: str):
        self.nome = nome
        self.idade = idade
        self.time = time

"""
nome: nome da pessoa
idade: idade da pessoa
time: time de futebol que a pessoa torce
"""

