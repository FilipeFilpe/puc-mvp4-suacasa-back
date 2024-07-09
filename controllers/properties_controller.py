from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import Property, Session, Visit
from schemas import (ErrorSchema, ListPropertiesSchema, PropertyDelSchema,
                     PropertySchema, PropertySearchSchema, PropertyViewSchema,
                     VisitSchema, show_properties, show_property)

property_tag = Tag(name="Propriedade", description="Adição, visualização e remoção de propriedades à base")
property_app = APIBlueprint('property_app', __name__)

@property_app.post('/properties', tags=[property_tag], responses={"200": PropertyViewSchema, "400": ErrorSchema, "400": ErrorSchema})
def add_property(form: PropertySchema):
    """Adiciona uma nova Propriedade à base de dados

    Retorna uma representação das propriedades.
    """
    _property = Property(
        title=form.title,
        address=form.address,
        value=form.value,        
        size=form.size,
        rooms=form.rooms,
        bathrooms=form.bathrooms,
        garages=form.garages,
        type=form.type,
        owner_id=form.owner_id,
        image=form.image,
    )
    logger.debug(f"Adicionando property de title: '{_property.title}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando property
        session.add(_property)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado property de title: '{_property.title}'")
        return show_property(_property), 201

    except IntegrityError as e:
        # como a duplicidade do title é a provável razão do IntegrityError
        error_msg = "Propriedade de mesmo título já salva na base :/"
        logger.warning(f"Erro ao adicionar propriedade '{_property.title}', {error_msg}")
        return {"message": error_msg}, 400

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar propriedade '{_property.title}', {error_msg}")
        return {"message": error_msg}, 400

@property_app.get('/properties', tags=[property_tag], responses={"200": ListPropertiesSchema, "404": ErrorSchema})
def get_properties():
    """Faz a busca por todos as Propriedades cadastrados

    Retorna uma representação da listagem de propriedades.
    """
    logger.debug("Coletando propriedades")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    properties = session.query(Property).all()

    if not properties:
        # se não há propriedades cadastrados
        return {"properties": []}, 200
    else:
        logger.debug("%d propriedades econtrados", len(properties))
        # retorna a representação de propriedade
        print(properties)
        return show_properties(properties), 200

@property_app.get('/property', tags=[property_tag], responses={"200": PropertyViewSchema, "404": ErrorSchema})
def get_property(query: PropertySearchSchema):
    """Faz a busca por uma Propriedade a partir do {id} da propriedade

    Retorna uma representação da propriedade.
    """
    property_id = query.id
    logger.debug(f"Coletando dados sobre propriedade #{property_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    _property = session.query(Property).filter(Property.id == property_id).first()

    if not _property:
        # se o property não foi encontrado
        error_msg = "Propriedade não encontrado na base :/"
        logger.warning(f"Erro ao buscar propriedade '{property_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Propriedade econtrada: '{_property.title}'")
        # retorna a representação de propriedade
        return show_property(_property), 200
    
@property_app.delete('/properties', tags=[property_tag], responses={"200": PropertyDelSchema, "404": ErrorSchema})
def del_property(query: PropertySearchSchema):
    """Deleta uma Propriedade a partir do id da propriedade informado
    Retorna uma mensagem de confirmação da remoção.
    """
    property_id = query.id
    print(property_id)
    logger.debug("Deletando dados sobre propriedade %s", property_id)
    # criando conexão com a base
    session = Session()
    with session.begin():
        # fazendo a remoção
        session.query(Visit).filter(Visit.property == property_id).delete()

        count = session.query(Property).filter(Property.id == property_id).delete()
        session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug("Deletado propriedade com id %s", property_id)
        return {"message": "Propriedade removida", "id": property_id}
    else:
        # se o propriedade não foi encontrado
        error_msg = "Propriedade não encontrado na base :/"
        logger.warning(f"Erro ao deletar propriedade #'{property_id}', {error_msg}")
        return {"message": error_msg}, 404

@property_app.post('/property/visit', tags=[property_tag], responses={"200": PropertyViewSchema, "404": ErrorSchema})
def add_visit(form: VisitSchema):
    """Adiciona de uma nova visita à uma propriedade cadastrada na base identificada pelo id

    Retorna uma representação da propriedade e visitas associadas.
    """
    property_id  = form.property_id
    logger.debug(f"Adicionando visitas a propriedade #{property_id}")
    session = Session()
    _property = session.query(Property).filter(Property.id == property_id).first()

    if not _property:
        error_msg = "Propriedade não encontrada na base :/"
        logger.warning(f"Erro ao adicionar visita a propriedade '{property_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando a visita
    visit = Visit(
        name=form.name,
        email=form.email,
        phone=form.phone,
        date=form.date,
    )

    # adicionando a visita a propriedade
    _property.add_visit(visit)
    session.commit()

    logger.debug(f"Adicionado visita a propriedade #{property_id}")

    # retorna a representação da propriedade
    return show_property(_property), 200


def properties():
  return property_app