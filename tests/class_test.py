import unittest
from courier import Courier
from order import Order
from valdec.errors import ValidationArgumentsError as ValidationError


class ClassesTypesTestCase(unittest.TestCase):
    def test_init_all_types(self):
        # провальный
        self.assertRaises(ValidationError, lambda: Courier(1, 2, 3, 4))
        self.assertRaises(ValidationError, lambda: Order('1', '2', '3', [4]))
        # верный
        Courier(1, 'car', [3], ["09:00-12:00", "16:00-21:30"])
        Order(1, 2., 3, ['9:00-12:00'])

    def test_init_list_parameters(self):
        # провальный
        self.assertRaises(
            (ValidationError,),
            lambda: Courier(1, '2', 3, '4')
        )
        self.assertRaises(
            (ValidationError,),
            lambda: Order(1, 2, 3, '3')
        )

    def test_init_int_parameters(self):
        # провальный
        self.assertRaises(
            (ValidationError,),
            lambda: Courier('1', '2', ['3'], ["09:00-12:00", "16:00-21:30"])
        )
        self.assertRaises(
            (ValidationError,),
            lambda: Order('1', '2', '3', ['9:00-12:00'])
        )

    def test_init_str_parameters(self):
        # провальный
        self.assertRaises(
            ValidationError,
            lambda: Courier(1, 2, [3], [4])
        )
        self.assertRaises(
            ValidationError,
            lambda: Order(1, 2, 3, [4])
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

    def test_init_weight_type(self):
        self.assertRaises(
            AssertionError,
            lambda: Order(1, 0.001, 3, ['9:00-12:00'])
            # too small and wrong accuracy
        )
        self.assertRaises(
            AssertionError,
            lambda: Order(1, 51, 3, ['9:00-12:00'])
            # too big
        )
        Order(1, 30, 3, ['9:00-12:00'])
        Order(1, 0.01, 3, ['9:00-12:00'])
        Order(1, 50, 3, ['9:00-12:00'])


if __name__ == '__main__':
    unittest.main()
