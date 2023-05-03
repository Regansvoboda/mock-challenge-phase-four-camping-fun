from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-signups',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship('Signup', backref='activity', cascade="all,delete, delete-orphan")
    campers = association_proxy('signups', 'camper')


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'
    
    # serialize_rules = ('-camper.signups', '-activities.signups',
    #                    '-camper.activities', '-activity.campers')

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))


    # @validates('time')
    # def validates_year(self, key, time_int):
    #     if 0> time >23:
    #         raise ValueError('must have an time between 8 and 18')
    #     return time_int


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-signups', 'activities')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship('Signup', backref='camper')
    activities = association_proxy('signups', 'activity')


    @validates('age')
    def validates_age(self, key, age):
        if age < 8:
            raise ValueError("Camper too young.")
        elif age > 18:
            raise ValueError("Camper too old.")
        return age
