import unittest
from unittest.mock import patch
from server.app.utils.util import Util

class TestUtil(unittest.TestCase):
    def test_get_uuid(self):
        uuid = Util.get_uuid()
        self.assertEqual(len(uuid), 36)
    
    def test_get_timestamp_ms(self):
        timestamp = Util.get_timestamp_ms()
        self.assertGreaterEqual(timestamp, 0)
    
    def test_write_to_temp_file(self):
        tempFile = 'test'
        temp = Util.write_to_temp_file(tempFile)
        self.assertEqual(temp, None)

