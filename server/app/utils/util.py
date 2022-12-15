import uuid
import datetime
from tempfile import NamedTemporaryFile


def write_to_temp_file(tempFile):
    temp = NamedTemporaryFile(delete=False)
    try:
        contents = tempFile.file.read()
        with temp as f:
            f.write(contents)
    except Exception as e:
        print("Exception:",e)
        return {"message": "There was an error uploading the file " + str(e)}
    finally:
        tempFile.file.close()
    return temp


def get_uuid():
    return str(uuid.uuid1())


def get_timestamp_ms():
    return int(datetime.datetime.now().timestamp())
