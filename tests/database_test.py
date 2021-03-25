import unittest
from database.db import *


def prepare_db():
    with open("/tmp/test.db", "w"):
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
        prepare_db()  # я без понятия почему тут ошибка, а дебаг бессилен
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
        self.assertTrue(data[0])
        self.assertEqual(data[-1], {"orders": [{"id": 1}, {"id": 2}, {"id": 3}]})


if __name__ == "__main__":
    unittest.main()
