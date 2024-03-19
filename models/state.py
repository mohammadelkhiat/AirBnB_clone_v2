#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # HBNB_TYPE_STORAGE can be “file” (FileStorage) or db (DBStorage)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref="state",
                              cascade="all, delete")
    else:
        @property
        def cities(self):
            ''' FileStorage relationship between State and City
            returns the list of City instances with state_id
            equals to the current State.id'''
            from models import storage
            from models.city import City
            city_list = []
            for city in list(storage.all(City).values()):
                if self.id == city.state_id:
                    city_list.append(city)
            return city_list