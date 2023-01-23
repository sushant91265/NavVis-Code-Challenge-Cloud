import unittest
from tempfile import NamedTemporaryFile
from app.utils.util import get_uuid, get_timestamp_ms, write_to_temp_file

class TestUtil(unittest.TestCase):
    def test_get_uuid(self):
        uuid = get_uuid()
        self.assertEqual(len(uuid), 36)
    
    def test_get_timestamp_ms(self):
        timestamp = get_timestamp_ms()
        self.assertGreaterEqual(timestamp, 0)

    def test_write_to_temp_file_exception_case(self):
        tempFile = NamedTemporaryFile(delete=False)
        tempFile.write(b'Hello World')
        tempFile.close()
        temp = write_to_temp_file(tempFile)
        self.assertEqual(temp, {'message': 'There was an error uploading the file read of closed file'})

    def test_write_to_temp_file(self):
        tempFile = NamedTemporaryFile(delete=False)
        tempFile.write(b'Hello World')
        temp = write_to_temp_file(tempFile)
        self.assertEqual(temp.__sizeof__(), 32)
        #self.assertEqual(temp.read(), b'Hello World')
        tempFile.close()
    
if __name__ == '__main__':
    unittest.main()