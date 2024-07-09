from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model import Base, Visit


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True)
    address = Column(String(150))
    value = Column(Float)
    size = Column(Float)
    rooms = Column(Integer)
    bathrooms = Column(Integer)
    garages = Column(Integer)
    type = Column(String(100))
    image = Column(String(500))

    visits = relationship("Visit", cascade="all,delete", backref="parent")
    owner_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    owner = relationship("Client")

    created_at = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        title:str,
        address:str,
        value:float,
        size: float,
        rooms: int,
        bathrooms: int,
        garages: int,
        type: str,
        image: str,
        owner_id:int,
        created_at:Union[DateTime, None] = None
    ):
        """
        Creata a Property

        Arguments:
            title: property title to show in app
            address: property location
            value: property value
            size: property size
            rooms: property rooms
            bathrooms: property bathrooms
            bathgaragesrooms: property garages
            owner_id: property owner
            created_at: created date in database
        """
        self.title = title
        self.address = address
        self.value = value
        self.size = size
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.garages = garages
        self.type = type
        self.owner_id = owner_id
        self.image = image

        # se não for informada, será o data exata da inserção no banco
        if created_at:
            self.created_at = created_at
    
    def add_visit(self, visit:Visit):
        """ Adiciona uma nova visita à Propriedade
        """
        self.visits.append(visit)
