"""
Declares the Base Model by augmenting the declarative_base
"""

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer

class Base(object):


    @declared_attr
    def __tablename__(cls):
        """don't have to specify table name in inherited classes"""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(cls=Base)


