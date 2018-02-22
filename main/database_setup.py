import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class PostData(Base):
    __tablename__ = 'postData'
    id = Column(Integer, primary_key=True)
    data = Column(String(250), nullable=False)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    categoryItems = relationship("CategoryItem",
                                 cascade='save-update, merge, delete')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object in serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            }

class CategoryDate(Base):
    __tablename__ = 'categorydate'
    date = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
        'date': self.date,
        'id': self.id,
        }

class CategoryItem(Base):
    __tablename__ = 'categoryitem'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'))
    # categories = relationship(Categories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily seralizeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
        }



engine = create_engine('sqlite:///catalogwithusers.db')

Base.metadata.create_all(engine)
