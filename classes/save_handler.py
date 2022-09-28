import json
import os.path


class SaveHandler:
    def __init__(self, file: str = "save_data.json"):
        self.file = file
        if not os.path.exists(self.file):
            with open(self.file, 'w') as file:
                print("test")
                json.dump({}, file)

    def has_save(self, key: str) -> bool:
        with open(self.file, 'r') as file:
            if key in json.load(file):
                return True
            else:
                return False

    def get_save(self, key: str) -> str:
        with open(self.file, 'r') as file:
            return json.load(file)[key]

    def set_save(self, key: str, value: str):
        with open(self.file, 'r') as file:
            data = json.load(file)
            data[key] = value
        with open(self.file, 'w') as file:
            json.dump(data, file)

    def delete_save(self, key: str):
        with open(self.file, 'r') as file:
            data = json.load(file)
            data.pop(key, None)
        with open(self.file, 'w') as file:
            json.dump(data, file)
