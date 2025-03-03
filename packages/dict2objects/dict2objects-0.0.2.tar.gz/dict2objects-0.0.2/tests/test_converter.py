import unittest
from dict2obj.converter import Dict2Obj

class TestDict2Obj(unittest.TestCase):

    def test_dict_to_object(self):
        data = {"name": "Alice", "age": 30, "details": {"city": "New York"}}
        obj = Dict2Obj(data)
        self.assertEqual(obj.name, "Alice")
        self.assertEqual(obj.age, 30)
        self.assertEqual(obj.details.city, "New York")

    def test_object_to_dict(self):
        data = {"name": "Alice", "age": 30}
        obj = Dict2Obj(data)
        self.assertEqual(obj.to_dict(), data)

    def test_to_dot_dict(self):
        data = {"name": "Alice", "details": {"city": "New York", "zip": 10001}}
        obj = Dict2Obj(data)
        expected_output = {
            "name": "Alice",
            "details.city": "New York",
            "details.zip": 10001
        }
        self.assertEqual(obj.to_dot_dict(), expected_output)

    def test_non_existent_key(self):
        data = {"name": "Alice"}
        obj = Dict2Obj(data)
        self.assertIsNone(obj.age)  # Accessing a non-existent key should return None
        self.assertIsNone(obj.details)  # Non-existent nested key should also return None

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Dict2Obj(["not", "a", "dict"])

if __name__ == "__main__":
    unittest.main()
