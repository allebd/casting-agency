from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)


#----------------------------------------------------------------------------#
# Movie Models.
#----------------------------------------------------------------------------#


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

#----------------------------------------------------------------------------#
# Actor Models.
#----------------------------------------------------------------------------#


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(120), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
