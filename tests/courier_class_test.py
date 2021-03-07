import unittest
from courier import Courier
from valdec.errors import ValidationArgumentsError as ValidationError


class CourierDataTestCase(unittest.TestCase):
    def test_init_all_types(self):
        # провальный
        self.assertRaises(ValidationError, lambda: Courier(1, 2, 3, 4))
        # верный
        Courier(1, 'car', [3], ["09:00-12:00", "16:00-21:30"])

    def test_init_list_parameters(self):
        # провальный
        self.assertRaises(
            (ValidationError,),
            lambda: Courier(1, '2', 3, '4')
        )

    def test_init_int_parameters(self):
        # провальный
        self.assertRaises(
            (ValidationError, ValueError),
            lambda: Courier('1', '2', ['3'], ["09:00-12:00", "16:00-21:30"])
        )

    def test_init_str_parameters(self):
        # провальный
        self.assertRaises(
            ValidationError,
            lambda: Courier(1, 2, [3], [4])
        )

    def test_init_courier_type(self):
        # провальные
        self.assertRaises(
            ValueError,
            lambda: Courier(1, 'ca', [1], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            ValueError,
            lambda: Courier(1, '1223', [1], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            ValueError,
            lambda: Courier(1, 'car1', [1], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            ValueError,
            lambda: Courier(1, 'feet', [1], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            ValueError,
            lambda: Courier(
                1, 'bik', [1], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            ValueError,
            lambda: Courier(
                1, 'boke', [1], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            ValueError,
            lambda: Courier(
                1, 'plane', [1], ["09:00-12:00", "16:00-21:30"])
        )
        # верные
        Courier(1, 'car', [1], ["09:00-12:00", "16:00-21:30"])
        Courier(2, 'foot', [1], ["09:00-12:00", "16:00-21:30"])
        Courier(3, 'bike', [1], ["09:00-12:00", "16:00-21:30"])


if __name__ == '__main__':
    unittest.main()
