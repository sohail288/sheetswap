from datetime import datetime

from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import validates, relationship

from passlib.apps import custom_app_context as sheetswap_pwd_context

from app.db import Base

"""
TODO: IMPLEMENT AN UPGRADABLE HASHING ROUTINE: https://pythonhosted.org/passlib/lib/passlib.context-tutorial.html
"""

class User(Base):
    __tablename__ = 'users'

    email = Column(Unicode(256), unique=True, nullable=False)
    username = Column(Unicode(256), unique=True, nullable=False)
    password_hash = Column(Unicode(32), nullable=False )
    admin =  Column(Boolean(), default=False)
    created_on = Column(DateTime(), default = datetime.now)
    updated_on = Column(DateTime(), default = datetime.now, onupdate=datetime.now)

    addresses = relationship('Address', back_populates='user')
    items = relationship('Item', back_populates='user')



    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address and len(address.split('@')) == 2
        return address


    @property
    def password(self):
        raise AttributeError("It is hashed.  The password.  Can't read it")

    @password.setter
    def password(self, password):
        self.password_hash = sheetswap_pwd_context.encrypt(password)

    def verify_password(self, password):
        return sheetswap_pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return "<User email={} admin={}>".format(self.email, self.admin)


class Address(Base):
    __tablename__ = 'addresses'

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='addresses')

    street_address = Column(Unicode(200))
    city = Column(Unicode(200))
    state = Column(Unicode(200))
    postal_code = Column(Unicode(200))
    country = Column(Unicode(200))

    def __repr__(self):
        return "<Address user={} street_address={} city={}>".format(self.user,
                                                                    self.street_address,
                                                                    self.city)

