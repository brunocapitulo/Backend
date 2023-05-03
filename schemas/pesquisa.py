from pydantic import BaseModel
from typing import Optional, List

from model.pesquisa import Pesquisa


class PesquisaSchema(BaseModel):
    """ Define as variváveis de uma tarefa
    """
    nome: str = "Bruno de Souza"
    time: str = "Clube de Regatas do Flamengo"
    idade: int = 26


class PesquisaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da pessoa
    """
    nome: str = "Bruno de Souza"


class ListagemPesquisaSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[PesquisaSchema]


def apresenta_pesquisa(pesquisas: List[Pesquisa]):
    """ Retorna uma representação da pesquisa
    """
    result = []
    for pesquisa in pesquisas:
        result.append({
            "nome": pesquisa.nome,
            "time": pesquisa.time,
            "idade": pesquisa.idade,
        })

    return {"pesquisas": result}


class PesquisaViewSchema(BaseModel):
    """ Define como uma pesquisa será retornada
    """
    id: int = 1
    nome: str = "Bruno de Souza"
    time: str = "Clube de Regatas do Flamengo"
    idade: int = 26


class PesquisaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str






 




