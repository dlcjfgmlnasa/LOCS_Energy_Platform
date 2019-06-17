# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Broken(Base):
    __tablename__ = 'broken'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    buildingId = Column(ForeignKey('building.id'), index=True)

    building = relationship('Building', primaryjoin='Broken.buildingId == Building.id', backref='brokens')


class Building(Base):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    overview = Column(String(255))


class Migration(Base):
    __tablename__ = 'migrations'

    id = Column(Integer, primary_key=True)
    timestamp = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)


class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    api_key = Column(String(100), nullable=False)
    filename = Column(String(100), nullable=False)
    filepath = Column(String(200), nullable=False)
    learning_percent = Column(Float)
    learning_log = Column(String(200))
    learning_status = Column(ENUM('STOP', 'LEARNING', 'COMPLETE', 'FAILURE'), nullable=False, server_default=FetchedValue())
    target = Column(ENUM('BROKEN', 'POWER'), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    updatedAt = Column(DateTime, nullable=False, server_default=FetchedValue())
    buildingId = Column(ForeignKey('building.id'), index=True)

    building = relationship('Building', primaryjoin='Model.buildingId == Building.id', backref='models')


class Power(Base):
    __tablename__ = 'power'

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
