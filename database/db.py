from valdec.errors import ValidationArgumentsError as ValidationError
from misc.useful_functions import rcf_now, parse_rcf, datetime_as_int
from misc.backpack_problem import solution as orders_dispense
from api.candy_flask import flask_application
from flask_sqlalchemy import SQLAlchemy
from objects.courier import Courier
from objects.order import Order


DATABASE_PATH = "/tmp/test.db"

# application config
flask_application.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{DATABASE_PATH}"  # сохраняем путь к бд
flask_application.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # убираем предупреждения об устаревших методах

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
DateTime = database.DateTime

# таблица для хранения соотвествий между курьрами их временем работы
couriers_hours_relationship = Table(
    "couriers_hours",
    Column("courier_id", Integer, ForeignKey("couriers.id")),
    Column("hours_id", Integer, ForeignKey("hours.id")),
)

# таблица для хранения соотвествий между курьерами и регионами, в которых работают курьеры
couriers_regions_relationship = Table(
    "couriers_regions",
    Column("courier_id", Integer, ForeignKey("couriers.id")),
    Column("region_id", Integer, ForeignKey("regions.id")),
    Column("number_of_divorces", Integer, default=0),
    Column("average_time", Float, default=0),
)

# таблица для хранения соотвествий между заказами и временем, в которые можно доставить заказ
orders_hours_relationship = Table(
    "orders_hours",
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("hours_id", Integer, ForeignKey("hours.id")),
)


def courier_to_json(courier):
    return {
        "courier_id": courier.id,
        "courier_type": courier.type,
        "regions": list(map(lambda x: x.region, courier.regions)),
        "working_hours": list(map(lambda x: x.hours, courier.working_hours)),
    }


# таблица курьеров
class CouriersTable(Model):
    __tablename__ = "couriers"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=False)
    type = Column(String(4), nullable=False)
    working_hours = Relationship("HoursTable", secondary=couriers_hours_relationship)
    regions = Relationship("RegionsTable", secondary=couriers_regions_relationship)
    workload = Column(Float, nullable=False)
    number_of_divorces = Column(Integer)
    earnings = Column(Integer)
    orders = Relationship("OrdersTable", backref="courier", lazy=True)

    def __repr__(self):
        return f"""
id {self.id}
type {self.type}
working_hours {list(map(lambda x: x.hours, self.working_hours))}
regions {list(map(lambda x: x.region, self.regions))}
workload {self.workload}
number_of_divorces {self.number_of_divorces}
earning {self.earnings}
orders {self.orders}
"""


# таблица заказов
class OrdersTable(Model):
    __tablename__ = "orders"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=False)
    weight = Column(Float, nullable=False)
    region = Column(Integer)
    delivery_hours = Relationship("HoursTable", secondary=orders_hours_relationship)
    # time
    post_time = Column(String(33), nullable=False)
    assign_time = Column(String(33), nullable=True)
    complete_time = Column(String(33), nullable=True)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=True)

    def __repr__(self):
        return f"""
id {self.id}
weight {self.weight}
region {self.region}
post_time {self.post_time}
delivery_hours {list(map(lambda x: x.hours, self.delivery_hours))}
post_time {self.post_time}
assign_time {self.assign_time}
complete_time  {self.complete_time}
courier_id = {self.courier_id}
"""


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
        return f"{self.region}"


def new_region(region):
    """Создает новый регион (но не сохраняет изменения)

    Args:
        region (int): Значение региона

    Returns:
        RegionsTable: обьект региона в базе данных
    """
    r = RegionsTable(region=region)
    return r


def load_region(region):
    """ "Подгружает" регион: если его не сущетвует, то создает, иначе возвращает ранее созданный

    Args:
        region (int): Значение региона

    Returns:
        RegionsTable: Обьект региона в базе данных
    """
    db_region = RegionsTable.query.filter_by(
        region=region
    ).first()  # пытаемся найти регион в бд
    if db_region:
        return db_region
    else:  # если не сущетствует, создаем новый
        return new_region(region)


def load_regions(regions):
    """Подгружает регионы, создает отсуствующие, находит старые

    Args:
        regions (List[int]): Массив регионов (их численных значений)

    Returns:
        List[RegionsTable]: Массив обьектов регионов
    """
    return [load_region(region) for region in regions]  # загружаем все регионы в бд


def new_hour(hour):
    """Создает новые часы (но не сохраняет изменения)

    Args:
        hour (str): Значение часов

    Returns:
        HoursTable: обьект часов в базе данных
    """
    h = HoursTable(hours=hour)
    return h


def load_hour(hour):
    """ "Подгружает" часы: если их не сущетвует, то создает, иначе возвращает ранее созданные

    Args:
        hour (str): Значение региона

    Returns:
        HoursTable: Обьект часов в базе данных
    """
    db_hour = HoursTable.query.filter_by(hours=hour).first()  # пытаемся найти часы в бд
    if db_hour:
        return db_hour
    else:  # если не нашли, создаем новые
        return new_hour(hour)


def load_hours(hours):
    """Подгружает часы, создает отсуствующие, находит старые

    Args:
        hours (List[str]): Массив часов (их строковых значений)

    Returns:
        List[HoursTable]: Массив обьектов часов
    """
    return [load_hour(hour) for hour in hours]


def save_courier(courier):
    """Сохраняет курьера в базу данных
    (не сохраняет изменения)
    Args:
        courier (Courier): обьект класса Курьер
    """
    id = courier.id
    type = courier.courier_type
    hours = courier.working_hours
    regions = courier.regions

    hours = load_hours(hours)
    regions = load_regions(regions)

    c = CouriersTable(
        id=id,
        type=type,
        working_hours=hours,
        regions=regions,
        workload=0.0,
        number_of_divorces=0,
        earnings=0,
    )
    # добавляем обьект курьера в базу данных
    # это также добавит все связи, те регионы и часы
    # которые были привязанны к этому курьеру
    database.session.add(c)


def save_couriers(couriers):
    """Сохраняет курьеров в базу данных и сохраняет изменения

    Args:
        couriers (List[Couriers]): массив курьеров
    """
    for courier in couriers:
        save_courier(courier)

    # сохраняем изменения
    database.session.commit()


def add_new_couriers(couriers):
    """Добавляет в базу данных новых курьеров

    Args:
        couriers (List[dict]): Данные из JSON

    Returns:
        Tuple[bool, dict]: Возвращет кортеж из двух значений: статус операции (успех?) и результат операции:
        Если операция прошла успешна, вернет массив успешно прошедних id
        Если операция проленна, вернет список проваленных id
    """
    data_to_save = []
    successful = []
    failed = []

    for courier_data in couriers:
        c_id = courier_data["courier_id"]

        try:
            type = courier_data["courier_type"]
            regions = courier_data["regions"]
            hours = courier_data["working_hours"]

            new_courier = Courier(c_id, type, regions, hours)

        except (
            KeyError,  # некоторые параметры отсуствуют в json
            ValidationError,  # некоторые параметры не прошли валидацию типов
            ValueError,  # некоторые параметры не прошли валидацию по значению
        ):
            failed.append(c_id)  # добавляет к проваленным
        else:
            successful.append(c_id)  # добавляем к успешнам
            data_to_save.append(new_courier)  # и в базу данных

    if failed:  # если был хотя бы один провальный
        return False, {
            "validation_error": {"couriers": [{"id": c_id} for c_id in failed]}
        }
    else:  # все успешные
        save_couriers(data_to_save)
        return True, {"couriers": [{"id": c_id} for c_id in successful]}


def update_courier_info(c_id, parameter):
    """Обновлят инфомарцию о курьере, и сохраняет изменения

    Args:
        c_id (int): ID курьеров
        parameter (Dict): словарь параметр: новое_значние

    Returns:
        Tuple[bool, dict]: Возвращет кортеж из двух значений: статус операции (успех?) и результат операции:
        Если операция прошла успешна, вернет JSON-вид обновленного обьекта
        Если операция проленна, вернет пустой словарь
    """
    if list(parameter.keys())[0] in [
        "courier_id",
        "courier_type",
        "regions",
        "working_hours",
    ]:  # проверяем, является ли параметр изменяемым
        data = CouriersTable.query.filter_by(id=c_id).first()  # получаем курьера из бд
        try:
            regions = []  # распаковываем регионы из бд
            for i in data.regions:
                regions.append(i.region)

            hours = []  # распаковываем часы из бд
            for i in data.working_hours:
                hours.append(i.hours)

            c = Courier(data.id, data.type, regions, hours)  # создает обьект курьера
            c.config(parameter)  # обновляем обьект, проходя через все валидации

            # обновляем данные
            data.id = c.id
            data.regions = load_regions(c.regions)
            data.working_hours = load_hours(c.working_hours)
            data.type = c.courier_type
            # сохраняем изменения
            database.session.commit()
        except (ValueError, AssertionError):
            return False, {}
        else:
            return True, courier_to_json(CouriersTable.query.filter_by(id=c_id).first())
    else:
        return False, {}


def save_order(order):
    """Сохраняет заказ в базу данных
    (не сохраняет изменения)
    Args:
        order (Order): обьект класса Курьер
    """
    o_id = order.id
    weight = order.weight
    hours = order.delivery_hours
    region = order.region

    hours = load_hours(hours)
    region = load_region(region)

    database.session.add(region)
    database.session.commit()

    o = OrdersTable(
        id=o_id,
        weight=weight,
        region=region.id,
        delivery_hours=hours,
        post_time=rcf_now(),
    )

    database.session.add(o)


def save_orders(orders):
    """Сохраняет заказы в базу (и сохраняем изменения)

    Args:
        orders (List[Order]): массив заказов
    """
    for order in orders:
        save_order(order)

    database.session.commit()


def add_new_orders(orders):
    """Добавляет в базу данных новых курьеров

    Args:
        orders (List[dict]): Данные из JSON

    Returns:
        Tuple[bool, dict]: Возвращет кортеж из двух значений: статус операции (успех?) и результат операции:
        Если операция прошла успешна, вернет массив успешно прошедних id
        Если операция проленна, вернет список проваленных id
    """
    data_to_save = []
    successful = []
    failed = []

    for orders_data in orders:
        o_id = orders_data["order_id"]

        try:
            weight = orders_data["weight"]
            region = orders_data["region"]
            hours = orders_data["delivery_hours"]

            new_order = Order(o_id, weight, region, hours)

        except (
            KeyError,  # некоторые параметры отсуствуют в json
            ValidationError,  # некоторые параметры не прошли валидацию типов
            ValueError,  # некоторые параметры не прошли валидацию по значению
        ):
            failed.append(o_id)  # добавляет к проваленным
        else:
            successful.append(o_id)  # добавляем к успешнам
            data_to_save.append(new_order)  # и в базу данных

    if failed:  # если был хотя бы один провальный
        return False, {
            "validation_error": {"orders": [{"id": c_id} for c_id in failed]}
        }
    else:  # все успешные
        save_orders(data_to_save)
        return True, {"orders": [{"id": c_id} for c_id in successful]}


def add_courier_orders(courier_id):
    courier_db = CouriersTable.query.filter_by(id=courier_id).first()
    # находим курьера к которому будет добавлять заказы
    if not courier_db:
        return False, {}

    courier_data = courier_to_json(courier_db)

    courier = Courier(
        courier_data["courier_id"],
        courier_data["courier_type"],
        courier_data["regions"],
        courier_data["working_hours"],
    )

    # находим заказы удовлетворяющие условиям
    all_orders = [
        Order(
            order_id=order.id,
            weight=order.weight,
            region=int(RegionsTable.query.filter_by(id=order.region).first().region),
            delivery_hours=list(map(lambda x: x.hours, order.delivery_hours)),
            additional_data={
                "post_time": order.post_time,
                "assign_time": order.assign_time,
            },
        )
        for order in OrdersTable.query.all()
    ]
    orders = list(filter(lambda order: order.config["assign_time"] is None, all_orders))
    orders = list(filter(lambda order: courier.can_take(order), orders))

    if not orders:
        return True, {}

    # формируем словарь значений id <-> параметры, для эффективного распределения заказов
    orders_values = {
        order.id: (
            int(order.weight * 100),  # минимальный вес 0.01
            datetime_as_int(parse_rcf(order.config["post_time"])),
        )
        for order in orders
    }

    orders_id = orders_dispense(orders_values, int(courier.free_load_capacity * 100))

    if not orders_id:
        return True, {}

    assign_time = rcf_now()

    # обновляем базу данных
    orders_db = []
    for o_id in orders_id:
        o = OrdersTable.query.filter_by(id=o_id).first()
        o.assign_time = assign_time
        o.courier_id = courier_db.id
        orders_db.append(o)
        database.session.add(o)

    courier_db.orders = orders_db
    database.session.add(courier_db)
    database.session.commit()

    return True, {
        "orders": [{"id": o_id} for o_id in orders_id],
        "assign_time": assign_time,
    }


def orders_complete(order_data):
    courier_id = order_data["courier_id"]
    order_id = order_data["order_id"]
    complete_time = order_data["complete_time"]

    order_db = OrdersTable.query.filter_by(id=order_id).first()

    if not order_db:
        return False, {}

    if order_db.courier_id != courier_id:
        return False, {}

    courier_db = CouriersTable.query.filter_by(id=courier_id).first()

    if not courier_db:
        return False, {}

    order_db.complete_time = complete_time

    start = parse_rcf(order_db.assign_time)
    end = parse_rcf(order_db.complete_time)

    delta = (end - start).seconds

    crr = database.session.query(couriers_regions_relationship).filter_by(
        courier_id=courier_id, region_id=order_db.region
    ).first()

    crr_courier_id, crr_region_id, crr_average_time, crr_number_of_divorces = crr

    crr_average_time = (
        crr.average_time * crr_number_of_divorces + delta
    ) / (crr_number_of_divorces + 1)
    crr_number_of_divorces += 1

    database.session.query(couriers_regions_relationship).filter_by(
        courier_id=courier_id, region_id=order_db.region
    ).update({"average_time": crr_average_time, "number_of_divorces": crr_number_of_divorces})
    database.session.add(order_db)
    database.session.add(courier_db)

    database.session.commit()

    return True, {"order_id": order_id}


def courier_info():
    pass
