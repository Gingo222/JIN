import inject
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from daily_jira.dependencies import (Config, MainDBSession)


inject.configure(dependencies.bind, bind_in_runtime=False)
session = inject.instance(MainDBSession)

# 创建对象的基类:
Base = declarative_base()
Base.metadata.bind = create_engine(inject.instance(Config).SQLALCHEMY_DATABASE_URI)

