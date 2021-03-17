from flask import Flask
from flask_sqlalchemy import SQLAlchemy

flask_application = Flask(__name__)
flask_application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
flask_application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = SQLAlchemy(flask_application)

Table = database.Table
Model = database.Model
Column = database.Column
Relationship = database.relationship
ForeignKey = database.ForeignKey

Integer = database.Integer
String = database.String
Float = database.Float


couriers_hours_relationship = Table(
    'couriers_hours',
    Column('courier_id', Integer, ForeignKey('couriers.id')),
    Column('hours_id', Integer, ForeignKey('hours.id'))
)

couriers_regions_relationship = Table(
    'couriers_regions',
    Column('courier_id', Integer, ForeignKey('couriers.id')),
    Column('region_id', Integer, ForeignKey('regions.id'))
)

orders_hours_relationship = Table(
    'orders_hours',
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('hours_id', Integer, ForeignKey('hours.id'))
)


class CouriersTable(Model):
    __tablename__ = 'couriers'
    id = Column(Integer, primary_key=True, unique=True)
    type = Column(String(4), nullable=False)
    working_hours = Relationship('HoursTable', secondary=couriers_hours_relationship)
    region = Relationship('RegionsTable', secondary=couriers_regions_relationship)
    workload = Column(Float, nullable=False)
    number_of_divorces = Column(Integer)
    earnings = Column(Integer)


class OrdersTable(Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, unique=True)
    weight = Column(Float, nullable=False)
    region = Column(Integer)
    delivery_hours = Relationship('HoursTable', secondary=orders_hours_relationship)


class HoursTable(Model):
    __tablename__ = 'hours'
    id = Column(Integer, primary_key=True, unique=True)
    hours = Column(String(11), nullable=False)


class RegionsTable(Model):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True, unique=True)
    region = Column(Integer, nullable=False)


with flask_application.app_context():
    database.create_all()
