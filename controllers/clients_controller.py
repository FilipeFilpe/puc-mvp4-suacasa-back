from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import Client, Property, Session, Visit
from schemas import (ClientDelSchema, ClientSchema, ClientSearchSchema,
                     ClientViewSchema, ErrorSchema, ListClientSchema,
                     show_client, show_clients)

client_tag = Tag(name="Clientes", description="Adição, visualização e remoção do dono de clientes à base")

client_app = APIBlueprint('client_app', __name__)

@client_app.post('/clients', tags=[client_tag], responses={"200": ClientViewSchema, "400": ErrorSchema, "400": ErrorSchema})
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
        return show_client(_client), 201

    except IntegrityError as e:
        # como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{_client.name}', {error_msg}")
        return {"message": error_msg}, 400

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{_client.name}', {error_msg}")
        return {"message": error_msg}, 400

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

@client_app.delete('/clients', tags=[client_tag], responses={"200": ClientDelSchema, "404": ErrorSchema})
def del_client(query: ClientSearchSchema):
    """Deleta um Cliente a partir do id do cliente informado
    Retorna uma mensagem de confirmação da remoção.
    """
    client_id = query.id
    print(client_id)
    logger.debug("Deletando dados sobre o cliente %s", client_id)
    # criando conexão com a base
    session = Session()
    with session.begin():
        # fazendo a remoção
        session.query(Property).filter(Property.owner_id == client_id).delete()

        count = session.query(Client).filter(Client.id == client_id).delete()
        session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug("Deletado cliente com id %s", client_id)
        return {"message": "Cliente removido", "id": client_id}
    else:
        # se o propriedade não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{client_id}', {error_msg}")
        return {"message": error_msg}, 404

def clients():
  return client_app