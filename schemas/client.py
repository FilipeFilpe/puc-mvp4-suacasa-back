from typing import List

from pydantic import BaseModel

from model.client import Client

name_base: str = "Filipe Sousa"
email_base: str = "example@email.com"
phone_base: str = "61981392999"


class ClientSchema(BaseModel):
    """ Define como um novo cliente é apresentado
    """
    name: str = name_base
    email: str = email_base
    phone: str = phone_base

class ClientViewSchema(BaseModel):
    """ Define como um cliente será retornado.
    """
    name: str = name_base
    email: str = email_base
    phone: str = phone_base
    properties: List[ClientSchema]

class ClientDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    title: str

class ClientSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da propriedade.
    """
    id: int = 1

class ClientWithIdSchema(ClientViewSchema):
    """ Define um novo client com id
    """
    id: int = 1

class ListClientSchema(BaseModel):
    """ Define como uma listagem de propriedades será retornada.
    """
    clients:List[ClientWithIdSchema]

def show_clients(clients: List[Client]):
    """ Retorna uma representação dos clientes seguindo o schema definido em
    ClientViewSchema.
    """
    result = []
    for client in clients:
        result.append({
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "properties": [
                {
                    "id": v.id,
                    "title": v.title,
                    "image": v.image,
                }
                for v in client.properties
            ],
        })
    
    return { "clients": result }

def show_client(client: Client):
    """ Retorna uma representação do cliente seguindo o schema definido em
    ClientWithIdSchema.
    """
    return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "properties": client.properties,
        }