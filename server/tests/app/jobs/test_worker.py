import sys
import unittest
sys.path.append('.')

from app.jobs import worker

class TestWorker(unittest.TestCase):
    def test_extract_numbers_positive_case(self):
        result = worker._extract_numbers(["+491234567890", "+491234567890", "+291234567891", "00491234567891"])
        self.assertEqual(result, ["+491234567890", "00491234567891"])
    
    def test_extract_numbers_empty_case(self):
        result = worker._extract_numbers([])
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()