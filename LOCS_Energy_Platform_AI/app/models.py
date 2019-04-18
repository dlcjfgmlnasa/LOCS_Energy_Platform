# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Building(Base):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    lat = Column(Float(asdecimal=True), nullable=False, server_default=FetchedValue())
    lng = Column(Float(asdecimal=True), nullable=False, server_default=FetchedValue())
    bld = Column(String(6), nullable=False, unique=True)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())

    def __repr__(self):
        return f'<Building id:{self.id} name:{self.name}>'


class Power(Base):
    __tablename__ = 'power'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    buildingId = Column(ForeignKey('building.id'), index=True)

    building = relationship('Building', primaryjoin='Power.buildingId == Building.id', backref='powers')

    def __repr__(self):
        return f'<Power id:{self.id}>'
