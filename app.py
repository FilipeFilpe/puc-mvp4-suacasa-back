import json
from urllib.parse import unquote

from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from sqlalchemy.exc import IntegrityError

from logger import logger
from model import *
from routes import add_client, add_property, clients, properties
from schemas import *

info = Info(title="Sua Casa API", version="1.0.0")
app = OpenAPI(__name__, info=info, static_url_path='/static')
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
property_tag = Tag(name="Propriedade", description="Adição, visualização e remoção de propriedades à base")
visit_tag = Tag(name="Visita", description="Adição de uma visita à uma propriedade cadastrada na base")

app.register_api(clients())
app.register_api(properties())

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

def loading_data():    
    session = Session()
    # add clients
    _client = session.query(Client).first()
    if(_client == None):
        with open('./initial_data.json', encoding='utf8') as json_file:
            _json = json.load(json_file)
            for client_json in _json['clients']:
                _client = Client(
                    name=client_json['name'],
                    email=client_json['email'],
                    phone=client_json['phone'], 
                )
                add_client(_client)

    # add properties
    _property = session.query(Property).first()
    if(_property == None):
        with open('./initial_data.json', encoding='utf8') as json_file:
            _json = json.load(json_file)
            for property_json in _json['properties']:
                _property = Property(
                    title=property_json['title'],
                    address=property_json['address'],
                    value=property_json['value'], 
                    size=property_json['size'],
                    rooms=property_json['rooms'],
                    bathrooms=property_json['bathrooms'],
                    garages=property_json['garages'],
                    type=property_json['type'],
                    owner=1,
                    thumbnail=property_json['thumbnail']
                )
                add_property(_property)

loading_data()