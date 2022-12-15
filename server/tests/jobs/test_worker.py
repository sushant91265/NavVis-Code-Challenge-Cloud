import unittest
from unittest.mock import patch
from db.models import Task, Result

from app.jobs import worker

class TestWorker(unittest.TestCase):
    def test_extract_numbers_49_case(self):
        result = worker._extract_numbers(["+4912345 678901", "+4912345678901", "+291234567891"])
        self.assertEqual(result, ["+4912345678901"])
    
    def test_extract_numbers_0049_case(self):
        result = worker._extract_numbers(["004912345678901", "004912345678901", "04912345678901", "+291234567891"])
        self.assertEqual(result, ["004912345678901"])

    def test_extract_numbers_empty_case(self):
        result = worker._extract_numbers([])
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()