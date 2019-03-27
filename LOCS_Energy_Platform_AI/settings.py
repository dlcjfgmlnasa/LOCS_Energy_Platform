# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


# DATABASES Setting values
DATABASES_ID = 'root'
DATABASES_PASSWORD = 'locslab'
DATABASES_HOST = '164.125.141.205'
DATABASES_PORT = '3306'
DATABASES_NAME = 'eprophet'
# dialect+driver://username:password@host:port/database
database_ref = f'mysql+pymysql://{DATABASES_ID}:{DATABASES_PASSWORD}' \
                f'@{DATABASES_HOST}:{DATABASES_PORT}/{DATABASES_NAME}?charset=utf8'

db_engine = create_engine(database_ref, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(db_engine)


def close_session():
    pass
