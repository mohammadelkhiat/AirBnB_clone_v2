#!/usr/bin/python3
''' This module defines a class to manage db storage for hbnb clone '''
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.user import User


class DBStorage:
    ''' This class manages storage of hbnb models in mysql database '''
    __engine = None
    __session = None

    def __init__(self):
        ''' configure the database '''
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        ''' query on the current database session
        all objects depending of the class name '''
        classes = [City, State, Review, Amenity, Place, User]
        result = {}
        objs = []
        if cls:
            objs += self.__session.query(cls).all()
        else:
            for a_class in classes:
                objs += self.__session.query(a_class).all()
        for obj in objs:
            key = f"{obj.__class__.__name__}.{obj.id}"
            result[key] = obj
        return result

    def new(self, obj):
        ''' add the object to the current database session '''
        self.__session.add(obj)

    def save(self):
        ''' commit all changes of the current database session '''
        self.__session.commit()

    def delete(self, obj=None):
        ''' delete from the current database session obj if not None '''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        ''' create all tables in the database (feature of SQLAlchemy) '''
        Base.metadata.create_all(self.__engine)
        session_f = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_f)