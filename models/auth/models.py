from datetime import datetime

from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import validates, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import Base



class User(Base):
    __tablename__ = 'users'

    email = Column(Unicode(256), unique=True, nullable=False)
    username = Column(Unicode(256), unique=True, nullable=False)
    password_hash = Column(Unicode(32), nullable=False )
    admin =  Column(Boolean(), default=False)
    created_on = Column(DateTime(), default = datetime.now)
    updated_on = Column(DateTime(), default = datetime.now, onupdate=datetime.now)

    addresses = relationship('Address', back_populates='user')


    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address and len(address) > 2
        return address


    @property
    def password(self):
        raise AttributeError("It is hashed.  The password.  Can't read it")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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

