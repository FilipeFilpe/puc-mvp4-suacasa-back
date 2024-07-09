from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag

from controllers import clients, properties
from logger import logger
from model import Client, Property, Session, Visit
from schemas import DashboardSchema, ErrorSchema, show_dashboard

info = Info(title="Sua Casa API", version="1.0.0")
app = OpenAPI(__name__, info=info, static_url_path='/static')
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
dash_tag = Tag(name="Dashboard", description="Dashboard com as principais informações da plataforma")

app.register_api(clients())
app.register_api(properties())

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/dashboard', tags=[dash_tag], responses={"200": DashboardSchema, "404": ErrorSchema})
def get_dashboard():
    """Faz a busca por todos os Clientes e Propriedades cadastrados
    
    Retorna uma representação do total de cada um.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clients = session.query(Client).count()
    properties = session.query(Property).count()
    visits = session.query(Visit).count()

    # retorna a representação de propriedade
    print(clients)
    return show_dashboard({"clients": clients, "properties": properties, "visits": visits}), 200