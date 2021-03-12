from valdec.errors import ValidationArgumentsError as ValidationError
from useful_functions import find_by
from courier import Courier
from order import Order


class OrderDispenser:
    def __init__(self):
        self.couriers = []
        self.inactive_orders = []

    def add_new_couriers(self, couriers_json: dict) -> (bool, dict):
        data = couriers_json['data']
        failed_ids = []
        success_ids = []

        for courier in data:
            try:
                id = courier['courier_id']

                find_same_id = False
                # проходим по всем уже записанным курьерам и
                # проверям уникальность нового id
                for c in self.couriers:
                    find_same_id = find_same_id or c.id == id

                if find_same_id:
                    raise ValueError('Not unique id')
                # 
                type = courier['courier_type']
                regions = courier['regions']
                working_hours = courier['working_hours']
                new_courier = Courier(id, type, regions, working_hours)
            except (
                    # если нету какого-то поля в json
                    KeyError,
                    # если какое-то значение не прошло валидацию по типу
                    ValidationError,
                    # если какое-то значение не прошло валидацию по значению
                    ValueError
            ):
                failed_ids.append(id)
            except Exception as unknown_exception:
                failed_ids.append(id)
                print('Unchecked Error:', unknown_exception)
            else:
                self.couriers.append(new_courier)
                success_ids.append(id)

        if failed_ids:  # есть провальные
            return False, {
                "validation_error": {
                    "couriers": [{'id': f_id} for f_id in failed_ids]
                }
            }
        else:
            return True, {
                "couriers": [{'id': s_id} for s_id in success_ids]
            }

    def patch_courier(self, id, patched_data: dict) -> (bool, dict):
        try:
            index = find_by(self.couriers, lambda courier: courier.id == id)
            type = patched_data.get('courier_type')
            regions = patched_data.get('regions')
            working_hours = patched_data.get('working_hours')
            if type:
                self.couriers[index].courier_type = type
            if regions:
                self.couriers[index].regions = regions
            if working_hours:
                self.couriers[index].working_hours = working_hours
        except (AssertionError, ValueError):
            return False, {}
        else:
            return True, self.couriers[index].to_dict()

    def add_new_orders(self, orders_json: dict) -> (bool, dict):
        data = orders_json['data']
        failed_ids = []
        success_ids = []

        for order in data:
            try:
                id = order['order_id']
                find_same_id = False
                for o in self.inactive_orders:
                    find_same_id = find_same_id or o.id == id

                if find_same_id:
                    raise ValueError('Not unique id')

                weight = order['weight']
                region = order['region']
                delivery_hours = order['delivery_hours']
                new_order = Order(id, weight, region, delivery_hours)
            except (
                    # если нету какого-то поля в json
                    KeyError,
                    # если какое-то значение не прошло валидацию по типу
                    ValidationError,
                    # если какое-то значение не прошло валидацию по значению
                    ValueError
            ):
                failed_ids.append(id)
            except Exception as unknown_exception:
                failed_ids.append(id)
                print('Unchecked Error:', unknown_exception)
            else:
                self.inactive_orders.append(new_order)
                success_ids.append(id)

        if failed_ids:  # есть провальные
            return False, {
                "validation_error": {
                    "orders": [{'id': f_id} for f_id in failed_ids]
                }
            }
        else:
            return True, {
                "orders": [{'id': s_id} for s_id in success_ids]
            }
