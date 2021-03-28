import unittest
from database.db import *
from time import sleep
from misc.useful_functions import rcf_now


def prepare_db():
    with open(DATABASE_PATH, "w"):
        pass

    with flask_application.app_context():
        database.create_all()


class DatabaseTestCase(unittest.TestCase):
    def test_adding_new_couriers(self):
        prepare_db()
        data = add_new_couriers(
            [
                {
                    "courier_id": 1,
                    "courier_type": "foot",
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"],
                },
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [22],
                    "working_hours": ["09:00-18:00"],
                },
                {
                    "courier_id": 3,
                    "courier_type": "car",
                    "regions": [12, 22, 23, 33],
                    "working_hours": [],
                },
            ]
        )
        self.assertTrue(data[0])
        self.assertEqual(data[-1], {"couriers": [{"id": 1}, {"id": 2}, {"id": 3}]})

    def test_patching_courier(self):
        prepare_db()
        add_new_couriers(
            [
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [22],
                    "working_hours": ["09:00-18:00"],
                },
            ]
        )
        data = update_courier_info(2, {"regions": [11, 33, 2]})
        self.assertTrue(data[0])
        self.assertEqual(
            data[-1],
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [11, 33, 2],
                "working_hours": ["09:00-18:00"],
            },
        )

    def test_adding_new_orders(self):
        prepare_db()
        data = add_new_orders(
            [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-18:00"],
                },
                {
                    "order_id": 2,
                    "weight": 15,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"],
                },
                {
                    "order_id": 3,
                    "weight": 0.01,
                    "region": 22,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"],
                },
            ]
        )
        sleep(3)
        add_new_orders(
            [
                {
                    "order_id": 20,
                    "weight": 5,
                    "region": 2,
                    "delivery_hours": ["09:00-10:00"],
                },
            ]
        )  # should have different timestamp
        sleep(1)
        self.assertTrue(data[0])
        self.assertEqual(data[-1], {"orders": [{"id": 1}, {"id": 2}, {"id": 3}]})

    def test_order_assign(self):
        prepare_db()
        add_new_couriers(
            [
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [1, 2, 3],
                    "working_hours": ["09:00-10:00", "11:00-12:00"],
                }
            ]
        )
        add_new_orders(
            [
                {
                    "order_id": 2,
                    "weight": 5,
                    "region": 2,
                    "delivery_hours": ["09:00-10:00"],
                },
            ]
        )
        sleep(1)
        add_new_orders(
            [
                {
                    "order_id": 3,
                    "weight": 5,
                    "region": 2,
                    "delivery_hours": ["09:00-10:00"],
                },
            ]
        )
        sleep(1)
        add_new_orders(
            [
                {
                    "order_id": 1,
                    "weight": 5,
                    "region": 2,
                    "delivery_hours": ["09:00-10:00"],
                },
            ]
        )
        data = add_courier_orders(2)
        self.assertTrue(data[0])
        self.assertEqual(
            sorted(data[-1]["orders"], key=lambda x: list(x.values())),
            [{"id": 1}, {"id": 2}, {"id": 3}],
        )

    def test_order_complete(self):
        prepare_db()
        add_new_couriers(
            [
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [1, 2, 3],
                    "working_hours": ["09:00-10:00", "11:00-12:00"],
                }
            ]
        )
        add_new_orders(
            [
                {
                    "order_id": 2,
                    "weight": 5,
                    "region": 2,
                    "delivery_hours": ["09:00-10:00"],
                },
            ]
        )
        add_courier_orders(2)
        sleep(10)
        data = orders_complete(
            {"courier_id": 2, "order_id": 2, "complete_time": rcf_now()}
        )

        self.assertTrue(data[0])
        self.assertEqual(data[1], {"order_id": 2})

    def test_courier_info(self):
        prepare_db()
        add_new_couriers(
            [
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [1, 2, 3],
                    "working_hours": ["09:00-10:00", "11:00-12:00"],
                }
            ]
        )
        data = courier_info(2)
        self.assertEqual(
            data,
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [1, 2, 3],
                "working_hours": ["09:00-10:00", "11:00-12:00"],
                "earnings": 0,
            },
        )

    def test_adding_order2(self):
        prepare_db()
        data = add_new_orders(
            [
                {
                    "order_id": 4,
                    "weight": 0.23,
                    "region": -1,
                    "delivery_hours": ["09:00-18:00"],
                },
                {
                    "order_id": 5,
                    "weight": 55,
                    "region": 2,
                    "delivery_hours": ["09:00-18:00"],
                },
                {
                    "order_id": 6,
                    "weight": 0.01,
                    "region": 5,
                    "delivery_hours": ["19:00-12:00", "16:00-21:30"],
                },
                {
                    "order_id": 7,
                    "weight": 0.01,
                    "region": 5,
                    "delivery_hours": [],
                },
            ]
        )
        self.assertEqual(
            data[1],
            {
                "validation_error": {
                    "orders": [{"id": 4}, {"id": 5}, {"id": 6}, {"id": 7}]
                }
            },
        )


if __name__ == "__main__":
    unittest.main()
