import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session


class Base:
    """Base class for ORM models.

    The actual base class, "Model" is generated with this class as its parent.
    """

    @declared_attr
    def __tablename__(cls):
        """Get the database table name based on the model name."""
        return cls.__name__.lower()


Model = declarative_base(cls=Base, name='Model')


class Database:
    def __init__(self, url=None, echo=False):
        # We need to import the models to update Model.metadata. We do it here
        # to avoid a circular reference since models imports this module.
        import application.models

        database_url = url or os.getenv('DATABASE_URL')
        assert database_url, 'DATABASE_URL environment variable not set.'
        self.engine = create_engine(database_url, echo=echo)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def create_all(self):
        Model.metadata.create_all(self.engine)

    def drop_all(self):
        Model.metadata.drop_all(self.engine)

    def cleanup(self):
        self.session.remove()
        self.engine.dispose()
