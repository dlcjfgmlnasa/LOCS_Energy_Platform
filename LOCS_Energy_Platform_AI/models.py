# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Building(db.Model):
    __tablename__ = 'building'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    lat = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.FetchedValue())
    lng = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.FetchedValue())
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

    building = db.relationship('Building', primaryjoin='Power.buildingId == Building.id', backref='powers')
