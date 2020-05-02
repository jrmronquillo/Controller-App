import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stb(Base):
    __tablename__ = 'stbInfo'
    id = Column(Integer, primary_key=True)
    mac = Column(String(250), nullable=False)
    slot = Column(String(250), nullable=False)
    model = Column(String(250), nullable=False)
    rackslot_id = Column(String(250), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'mac': self.mac,
            'slot': self.slot,
            'rackslot_id': self.rackslot_id,
            'model': self.model,
            }

class RackSlot(Base):
    __tablename__='rackInfo'
    id = Column(Integer, primary_key=True)
    rackNumber = Column(String(250), nullable=False)
    irnetboxMac = Column(String(250), nullable=False)
    slot = Column(String(250), nullable=False)
    videoRoute = Column(String(250), nullable=False)
    stbModel = Column(String(250), nullable=False)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'rackNumber': self.rackNumber,
            'irnetboxMac': self.irnetboxMac,
            'slot': self.slot,
            'videoRoute': self.videoRoute,
            'stbModel': self.stbModel,
            }


engine = create_engine('sqlite:///stbInfo.db')

Base.metadata.create_all(engine)
