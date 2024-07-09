from pydantic import BaseModel


class DashboardSchema(BaseModel):
    """ Define como a dashboard é apresentada
    """
    clients: int = 150
    properties: int = 150
    visits: int = 250

def show_dashboard(dashboard):
    """ Retorna uma representação do dasbhboard o schema definido.
    """
    return {
      "clients": dashboard['clients'],
      "properties": dashboard['properties'],
      "visits": dashboard['visits'],
    }