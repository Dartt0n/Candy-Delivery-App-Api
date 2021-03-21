import re
from flask_sqlalchemy import SQLAlchemy
from api.candy_flask import flask_application
from objects.courier import Courier

DATABASE_PATH = "/tmp/test.db"

# application config
flask_application.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
flask_application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# database file
database = SQLAlchemy(flask_application)

# # # # for clean code # # # #

# table objects
Table = database.Table
Model = database.Model
Column = database.Column
Relationship = database.relationship
ForeignKey = database.ForeignKey
# types
Integer = database.Integer
String = database.String
Float = database.Float

# Дополнительная таблица для хранения соотвествий
# между курьрами их временем работы
couriers_hours_relationship = Table(
    "couriers_hours",
    Column("courier_id", Integer, ForeignKey("couriers.id")),
    Column("hours_id", Integer, ForeignKey("hours.id")),
)

# Дополнительная таблица для хранения соотвествий
# между курьерами и регионами, в которых работают курьеры
couriers_regions_relationship = Table(
    "couriers_regions",
    Column("courier_id", Integer, ForeignKey("couriers.id")),
    Column("region_id", Integer, ForeignKey("regions.id")),
)

# Дополнительная таблица для хранения соотвествий
# между заказами и временем, в которые можно доставить заказ
orders_hours_relationship = Table(
    "orders_hours",
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("hours_id", Integer, ForeignKey("hours.id")),
)


# таблица курьеров, которая содержит всю необходимую информацию
class CouriersTable(Model):
    __tablename__ = "couriers"
    id = Column(Integer, unique=True)
    type = Column(String(4), nullable=False)
    working_hours = Relationship("HoursTable", secondary=couriers_hours_relationship)
    region = Relationship("RegionsTable", secondary=couriers_regions_relationship)
    workload = Column(Float, nullable=False)
    number_of_divorces = Column(Integer)
    earnings = Column(Integer)

    def __repr__(self):
        return {
            "courier_id": self.id,
            "courier_type": self.type,
            "regions": self.regions,
            "working_hours": self.working_hours,
        }


# таблица заказов, с нужной информацией
class OrdersTable(Model):
    __tablename__ = "orders"
    id = Column(Integer, unique=True)
    weight = Column(Float, nullable=False)
    region = Column(Integer)
    delivery_hours = Relationship("HoursTable", secondary=orders_hours_relationship)

    def __repr__(self):
        return {
            "order_id": self.id,
            "weight": self.weight,
            "region": self.region,
            "delivery_hours": self.delivery_hours
        }


# таблица часов, для избежания дублирования данных
class HoursTable(Model):
    __tablename__ = "hours"
    id = Column(Integer, primary_key=True, unique=True)
    hours = Column(String(11), nullable=False)

    def __repr__(self):
        return self.hours

# таблица регионов, для избежания дублирования данных
class RegionsTable(Model):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, unique=True)
    region = Column(Integer, nullable=False)

    def __repr__(self):
        return self.region
