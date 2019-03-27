# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Sequence
from LOCS_Energy_Platform_AI.settings import db_session, Base, init_db


class Building(Base):
    __tablename__ = 'building'

    id = Column(Integer, Sequence('building_id_seq'), primary_key=True, name='id')
    name = Column(String(50), nullable=False, name='name')
    # longitude = Column(String(50), nullable=False, name='longitude')        # 경도
    # latitude = Column(String(50), nullable=False, name='latitude')          # 위도

    def __repr__(self):
        return f'<Building {self.id}:{self.name}>'


class Power(Base):
    __tablename__ = 'power'

    id = Column(Integer, Sequence('power_id_seq'), primary_key=True, nullable=False, name='id')
    building_id = Column(Integer, ForeignKey('building.id'), name='building_id')
    building = relationship('building', back_populates='power')
    year = Column(Integer, name='year')         # 년도
    month = Column(Integer, name='month')       # 월
    day = Column(Integer, name='day')           # 일
    hour = Column(Integer, name='hour')         # 시
    minute = Column(Integer, name='minute')     # 분

    def __repr__(self):
        return f'<Power id:{self.id} {self.year}-{self.month}-{self.day} {self.hour}:{self.minute}'


init_db()
instance = Building(name='Test Building')
