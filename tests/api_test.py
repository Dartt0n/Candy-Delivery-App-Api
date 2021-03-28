import unittest
from requests import post, patch, get

url = "http://yandexserver:8080/"


class ApiTestCase(unittest.TestCase):
    def test_post_couriers_valid(self):
        data = {
            "data": [
                {
                    "courier_id": 1,
                    "courier_type": "foot",
                    "regions": [1, 2, 3, 4, 5],
                    "working_hours": ["09:00-18:00"],
                },
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [3, 4, 5, 6, 7],
                    "working_hours": ["09:00-12:00", "10:00-13:00"],
                },
                {
                    "courier_id": 3,
                    "courier_type": "car",
                    "regions": [1, 2, 100],
                    "working_hours": ["09:00-12:00"],
                },
            ]
        }
        response = post(url + "couriers", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"couriers": [{"id": 1}, {"id": 2}, {"id": 3}]}
        )

    def test_post_couriers_invalid(self):
        data = {
            "data": [
                {
                    "courier_id": 4,
                    "courier_type": "feet",
                    "regions": [1, 2, 3, 4, 5],
                    "working_hours": ["09:00-18:00"],
                },
                {
                    "courier_id": 5,
                    "courier_type": "bike",
                    "regions": [-1, -2, -3],
                    "working_hours": ["09:00-12:00", "10:00-13:00"],
                },
                {
                    "courier_id": 6,
                    "courier_type": "car",
                    "regions": [1, 2, 100],
                    "working_hours": ["19:00-12:00"],
                },
            ]
        }
        response = post(url + "couriers", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"validation_error": {"couriers": [{"id": 4}, {"id": 5}, {"id": 6}]}},
        )

    def test_post_orders_valid(self):
        data = {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"],
                },
                {
                    "order_id": 2,
                    "weight": 15,
                    "region": 2,
                    "delivery_hours": ["09:00-18:00"],
                },
                {
                    "order_id": 3,
                    "weight": 0.01,
                    "region": 5,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"],
                },
            ]
        }
        response = post(url + "orders", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"orders": [{"id": 1}, {"id": 2}, {"id": 3}]})

    def test_post_orders_invalid(self):
        data = {
            "data": [
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
        }
        response = post(url + "orders", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "validation_error": {
                    "orders": [{"id": 4}, {"id": 5}, {"id": 6}, {"id": 7}]
                }
            },
        )

    def test_patch_courier(self):
        data = patch(
            url + "couriers/1",
            json={
                "courier_type": "bike",
            },
        )
        self.assertEqual(data.status_code, 200)
        self.assertEqual(
            data.json(),
            {
                "courier_id": 1,
                "courier_type": "bike",
                "regions": [1, 2, 3, 4, 5],
                "working_hours": ["09:00-18:00"],
            },
        )
        data = patch(
            url + "couriers/2",
            json={
                "courier_type": "car",
                "regions": [1, 2, 3, 4, 5],
            },
        )
        self.assertEqual(data.status_code, 200)
        dj = data.json()
        dj["regions"].sort()
        self.assertEqual(
            dj,
            {
                "courier_id": 2,
                "courier_type": "car",
                "regions": [1, 2, 3, 4, 5],
                "working_hours": ["09:00-12:00", "10:00-13:00"],
            },
        )
        data = patch(
            url + "couriers/3",
            json={
                "courier_type": "foot",
                "regions": [1, 2],
                "working_hours": ["09:00-18:00"],
            },
        )
        self.assertEqual(data.status_code, 200)
        self.assertEqual(
            data.json(),
            {
                "courier_id": 3,
                "courier_type": "foot",
                "regions": [1, 2],
                "working_hours": ["09:00-18:00"],
            },
        )

    def test_orders_assign(self):
        patch(
            url + "couriers/2",
            json={
                "regions": [1, 2, 3, 4, 5, 6, 7, 8, 9, 1000],
                "working_hours": ["01:00-23:00"],
                "courier_type": "bike",
            },
        )
        data = post(url + "orders/assign", json={"courier_id": 2})
        self.assertEqual(data.status_code, 200)
        self.assertEqual(data.json()["orders"], [{"id": 3}, {"id": 1}])


if __name__ == "__main__":
    unittest.main()
