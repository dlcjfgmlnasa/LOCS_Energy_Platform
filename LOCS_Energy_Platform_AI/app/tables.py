# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Enum
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Building(Base):
    __tablename__ = 'building'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    overview = Column(String(255))

    def __repr__(self):
        return f'<Building id:{self.id} name:{self.name} overview:{self.overview}>'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Power(Base):
    __tablename__ = 'power'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    pre_value = Column(Float)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    buildingId = Column(ForeignKey('building.id'), index=True)

    building = relationship('Building', primaryjoin='Power.buildingId == Building.id', backref='powers')

    def __repr__(self):
        return f'<Power id:{self.id}>'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Broken(Base):
    __tablename__ = 'broken'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    buildingId = Column(ForeignKey('building.id'), index=True)

    building = relationship('Building', primaryjoin='Broken.buildingId == Building.id', backref='brokens')

    def __repr__(self):
        return f'<Broken id:{self.id}>'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Model(Base):
    __tablename__ = 'model'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(Integer, primary_key=True)
    api_key = Column(String(100), nullable=False)
    filename = Column(String(100), nullable=False)
    filepath = Column(String(200), nullable=False)
    learning_percent = Column(Float)
    learning_log = Column(String(200))
    learning_status = Column(Enum('STOP', 'LEARNING', 'COMPLETE', 'FAILURE'), nullable=False, server_default=FetchedValue())
    target = Column(Enum('BROKEN', 'POWER'), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    buildingId = Column(ForeignKey('building.id'), index=True)

    building = relationship('Building', primaryjoin='Model.buildingId == Building.id', backref='models')

    def __repr__(self):
        return f'<Model id:{self.id}>'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
