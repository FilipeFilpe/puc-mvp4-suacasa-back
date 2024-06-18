from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import *
from schemas import *

client_tag = Tag(name="Clientes", description="Adição, visualização e remoção do dono de clientes à base")

client_app = APIBlueprint('client_app', __name__)

@client_app.post('/clients', tags=[client_tag], responses={"200": ClientViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_client(form: ClientSchema):
    """Adiciona um novo Cliente à base de dados

    Retorna uma representação do cliente.
    """
    _client = Client(
        name=form.name,
        email=form.email,
        phone=form.phone
    )
  
    logger.debug(f"Adicionando cliente de nome: '{_client.name}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando client
        session.add(_client)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cliente de nome: '{_client.name}'")
        return show_client(_client), 200

    except IntegrityError as e:
        # como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{_client.name}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{_client.name}', {error_msg}")
        return {"mesage": error_msg}, 400

@client_app.get('/clients', tags=[client_tag], responses={"200": ListClientSchema, "404": ErrorSchema})
def get_clients():
    """Faz a busca por todos os Clientes cadastrados
    
    Retorna uma representação da listagem de clientes.
    """
    logger.debug("Coletando clientes")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clients = session.query(Client).all()

    if not clients:
        # se não há clients cadastrados
        return {"clients": []}, 200
    else:
        logger.debug("%d clients econtrados", len(clients))
        # retorna a representação de propriedade
        print(clients)
        return show_clients(clients), 200

def clients():
  return client_app