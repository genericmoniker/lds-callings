from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger

from application.database import Model


class User(Model):
    """A user of the lds-callings application."""
    id = Column(Integer, primary_key=True)
    unit = Column(Integer)

    def tenant(self):
        return str(self.unit)


class Individual(Model):
    """An individual in a unit."""
    id = Column(BigInteger, primary_key=True)
    preferred_name = Column(String)


class Organization(Model):
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    name = Column(String)
    display_order = Column(Integer)


class Position(Model):
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer)  # custom positions are all 999999
    name = Column(String)
    display_order = Column(Integer)


class Calling(Model):
    id = Column(Integer, primary_key=True)
    individual_id = Column(Integer)
    position_id = Column(Integer)
    sustained = Column(DateTime)
    released = Column(Boolean)


