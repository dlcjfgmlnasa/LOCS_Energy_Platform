# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# dialect+driver://username:password@host:port/database
DATABASES_ID = 'root'
DATABASES_PASSWORD = 'locslab'
DATABASES_HOST = '164.125.141.205'
DATABASES_PORT = '3306'
DATABASES_NAME = 'eprophet'
DATABASES_REF = f'mysql+pymysql://{DATABASES_ID}:{DATABASES_PASSWORD}' \
                f'@{DATABASES_HOST}:{DATABASES_PORT}/{DATABASES_NAME}'

DATABASES_ENGINE = create_engine(DATABASES_REF, echo=True)
print(DATABASES_ENGINE)

