from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from model import Base


class Client(Base):
  __tablename__ = 'clients'

  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  email = Column(String(150), unique=True)
  phone = Column(String(11))
  created_at = Column(DateTime, default=datetime.now())

  properties = relationship("Property", cascade="all, delete")

  def __init__(
    self,
    name:str,
    email:str,
    phone:str,
    created_at:Union[DateTime, None] = None
  ):
    """
    Create a Client

    Arguments:
      name: client name
      email: client email
      phone: client phone
    """
    self.name = name
    self.email = email
    self.phone = phone

    # se não for informada, será o data exata da inserção no banco
    if created_at:
      self.created_at = created_at