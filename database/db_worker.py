from database.db_model import (
    RegionsTable,
    HoursTable,
    OrdersTable,
    CouriersTable,
    database,
)
from valdec.errors import ValidationArgumentsError as ValidationError
from objects.courier import Courier
from objects.order import Order


# TODO:   add_courier_orders,
# TODO:   orders_complete,
# TODO:   courier_info,


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
    db_region = RegionsTable.query.filter_by(region=region).first()
    if db_region:
        return db_region
    else:
        return new_region(region)


def load_regions(regions):
    """Подгружает регионы, создает отсуствующие, находит старые

    Args:
        regions (List[int]): Массив регионов (их численных значений)

    Returns:
        List[RegionsTable]: Массив обьектов регионов
    """
    return [load_region(region) for region in regions]


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
    db_hour = HoursTable.query.filter_by(hours=hour).first()
    if db_hour:
        return db_hour
    else:
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

    database.session.add(c)


def save_couriers(couriers):
    """Сохраняет курьеров в базу данных и сохраняет изменения

    Args:
        couriers (List[Couriers]): массив курьеров
    """
    for courier in couriers:
        save_courier(courier)
    database.commit()


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
        id = courier_data["courier_id":]

        try:
            type = courier_data["courier_type"]
            regions = courier_data["regions"]
            hours = courier_data["working_hours"]

            new_courier = Courier(id, type, regions, hours)

        except (
            KeyError,  # некоторые параметры отсуствуют в json
            ValidationError,  # некоторые параметры не прошли валидацию типов
            ValueError,  # некоторые параметры не прошли валидацию по значению
        ):
            failed.append(id)  # добавляет к проваленным
        else:
            successful.append(id)  # добавляем к успешнам
            data_to_save.append(new_courier)  # и в базу данных

    if failed:  # если был хотя бы один провальный
        return False, {
            "validation_error": {"couriers": [{"id": c_id} for c_id in failed]}
        }
    else:  # все успешные
        save_couriers(data_to_save)
        return True, {"couriers": [{"id": c_id} for c_id in successful]}


def update_courier_info(id, parameter):
    """Обновлят инфомарцию о курьере, и сохраняет изменения

    Args:
        id (int): ID курьеров
        parameter (Dict): словарь параметр: новое_значние

    Returns:
        Tuple[bool, dict]: Возвращет кортеж из двух значений: статус операции (успех?) и результат операции:
        Если операция прошла успешна, вернет JSON-вид обновленного обьекта
        Если операция проленна, вернет пустой словарь
    """
    if parameter.keys[0] in ["courier_id", "courier_type", "regions", "working_hours"]:
        data = CouriersTable.query.filter_by(id=id).first()
        try:
            c = Courier(**data)  # создает обьект курьера
            c.config(parameter)  # обновляем обьект, проходя через все валидации
            data.update(  # обновляем информацию в бд
                {
                    "id": c.id,
                    "type": c.courier_type,
                    "working_hours": load_hours(c.working_hours),
                    "regions": load_regions(c.regions),
                }
            )
        except (ValueError, AssertionError):
            return False, {}
        else:
            database.session.commit()
            return True, CouriersTable.query.filter_by(id=id).first()
    else:
        return False, {}


def save_order(order):
    """Сохраняет заказ в базу данных
    (не сохраняет изменения)
    Args:
        order (Order): обьект класса Курьер
    """
    id = order.id
    weight = order.weight
    hours = order.delivery_hours
    region = order.region

    hours = load_hours(hours)
    region = load_region(region)

    o = OrdersTable(
        id=id,
        weight=weight,
        region=region,
        delivery_hours=hours,
    )

    database.session.add(o)


def save_orders(orders):
    """Сохраняет курьеров в базу данных и сохраняет изменения

    Args:
        orders (List[Order]): массив курьеров
    """
    for order in orders:
        save_order(order)
    database.commit()


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
        id = orders_data["order_id"]

        try:
            weight = orders_data["weight"]
            region = orders_data["region"]
            hours = orders_data["delivery_hours"]

            new_order = Order(id, weight, region, hours)

        except (
            KeyError,  # некоторые параметры отсуствуют в json
            ValidationError,  # некоторые параметры не прошли валидацию типов
            ValueError,  # некоторые параметры не прошли валидацию по значению
        ):
            failed.append(id)  # добавляет к проваленным
        else:
            successful.append(id)  # добавляем к успешнам
            data_to_save.append(new_order)  # и в базу данных

    if failed:  # если был хотя бы один провальный
        return False, {
            "validation_error": {"orders": [{"id": c_id} for c_id in failed]}
        }
    else:  # все успешные
        save_couriers(data_to_save)
        return True, {"orders": [{"id": c_id} for c_id in successful]}