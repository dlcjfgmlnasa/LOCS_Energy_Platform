# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Building(db.Model):
    __tablename__ = 'building'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lat = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.FetchedValue())
    lng = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.FetchedValue())
    bld = db.Column(db.String(6), nullable=False, unique=True)
    createdAt = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updatedAt = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updatedAt = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    buildingId = db.Column(db.ForeignKey('building.id'), index=True)
    value = db.Column(db.Float, nullable=False)

    building = db.relationship('Building', primaryjoin='Power.buildingId == Building.id', backref='powers')
