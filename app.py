from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect
from flask_cors import CORS
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from model import Session, Pesquisa
from schemas.error import ErrorSchema
from schemas.pesquisa import PesquisaSchema, PesquisaBuscaSchema, ListagemPesquisaSchema, PesquisaDelSchema, PesquisaViewSchema, apresenta_pesquisa
from logger import logger


info = Info(title = 'Pesquisa Times de Futebol API', version = "1.0.0")
app = OpenAPI(__name__, info = info)
CORS(app)

#agora vamos definir as tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pesquisa_tag = Tag(name = "Adiciona Pesquisa", description = "Adiciona, visualiza e deleta uma pessoa na pesquisa")



@app.get('/', tags = [home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do tipo de documentação
    """
    return redirect('/openapi')



@app.post('/pesquisa', tags = [pesquisa_tag],
          responses = {"200": PesquisaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pesquisa(form: PesquisaSchema):
    """Adiciona uma nova Pesquisa à base de dados

    Retorna uma representação das pesquisas
    """
    pesquisa = Pesquisa(
        nome = form.nome,
        time = form.time,
        idade = form.idade)
    logger.debug(f"Adicionando pesquisa de nome: '{pesquisa.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pesquisa
        session.add(pesquisa)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pesquisa de nome: '{pesquisa.nome}'")
        return apresenta_pesquisa(pesquisa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pesquisa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pesquisa '{pesquisa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pesquisa '{pesquisa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400



@app.get('/pesquisas', tags = [pesquisa_tag],
         responses = {"200": ListagemPesquisaSchema, "404": ErrorSchema})
def get_pesquisa():
    """Faz a busca por todas as Pesquisas cadastrados

    Retorna uma representação da listagem de pesquisas
    """
    logger.debug(f"Coletando pesquisas")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pesquisas = session.query(Pesquisa).all()

    if not pesquisas:
        # se não há pesquisas cadastrados
        return {"pesquisas": []}, 200
    else:
        logger.debug(f"%d pesquisas encontradas" % len(pesquisas))
        # retorna a representação de pesquisa
        print(pesquisas)
        return apresenta_pesquisa(pesquisas), 200



@app.delete('/pesquisa', tags = [pesquisa_tag],
            responses = {"200": PesquisaDelSchema, "404": ErrorSchema})
def del_pesquisa(query: PesquisaBuscaSchema):
    """Deleta uma Pesquisa a partir do nome da pessoa informado

    Retorna uma mensagem de confirmação da remoção.
    """
    pesquisa_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre pesquisa #{pesquisa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Pesquisa).filter(Pesquisa.nome == pesquisa_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado pesquisa #{pesquisa_nome}")
        return {"mesage": "Pesquisa removida", "id": pesquisa_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Pesquisa não encontrada na base :/"
        logger.warning(f"Erro ao deletar pesquisa #'{pesquisa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404




