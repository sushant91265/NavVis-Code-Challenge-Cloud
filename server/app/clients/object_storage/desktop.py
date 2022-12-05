import os
import shutil


class DesktopOS:
    def __init__(self, path) -> None:
        self.path = path

    def put(self, name, file):
        path = os.path.expanduser(os.path.join(self.path, name))
        filepath = os.path.abspath(file.name)
        shutil.copyfile(filepath, path)
        return {"status": "success", "path": path}

    def get(self, path):
        filepath = os.path.expanduser(os.path.join(self.path, path))
        with open(os.path.expanduser(filepath), "r") as file:
            return file.readlines()

    def delete(self, path):
        filepath = os.path.expanduser(os.path.join(self.path, path))
        shutil.rmtree(filepath)
        return True