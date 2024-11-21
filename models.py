from sqlalchemy import Column, String, Boolean, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Evento(Base):
    __tablename__ = 'eventos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    usuario = Column(String, index=True)
    accion = Column(String)
    archivo = Column(String, nullable=True)
    autorizacion = Column(Boolean, default=False)
    ubicacion = Column(String, nullable=True)
    out_of_hours = Column(Boolean, default=False)
    destination = Column(String, nullable=True)
    device = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    software = Column(String, nullable=True)
