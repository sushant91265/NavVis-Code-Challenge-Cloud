import unittest
from app.utils import get_uuid, get_timestamp_ms, write_to_temp_file

class TestUtil(unittest.TestCase):
    def test_get_uuid(self):
        uuid = get_uuid()
        self.assertEqual(len(uuid), 36)
    
    def test_get_timestamp_ms(self):
        timestamp = get_timestamp_ms()
        self.assertGreaterEqual(timestamp, 0)
    
    def test_write_to_temp_file(self):
        tempFile = 'test'
        temp = write_to_temp_file(tempFile)
        self.assertEqual(temp, None)

