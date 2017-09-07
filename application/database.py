import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Model = declarative_base(cls=Base)


class Database:
    def __init__(self):
        # Import models here to update Model.metadata while avoiding a circular
        # reference.
        import application.models

        database_url = os.getenv('DATABASE_URL')
        assert database_url, 'DATABASE_URL environment variable not set.'
        self.engine = create_engine(database_url)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def create_all(self):
        Model.metadata.create_all(self.engine)
