import json
import os


class ConfigHandler:

    # class attributes that are not accessed dynamically
    _class_attributes = [
        '_path',
        '_store',
        '_file_content',
    ]

    # path for config file
    _path: str

    # dict to hold parsed config file
    _store: dict

    def __init__(self, path: str) -> None:
        self._path = path
        self._load_store_from_file()

    def _get_file_handler(self):
        try:
            return open(self._path)
        except OSError:
            return open(self._path, 'w')

    @property
    def _file_content(self) -> str:
        file_handler = self._get_file_handler()
        contents = file_handler.read()
        file_handler.close()
        return contents

    @_file_content.setter
    def _file_content(self, contents: str) -> None:
        try:
            # delete config backup file
            os.remove("{}.backup".format(self._path))
        except FileNotFoundError:
            """
            no-op because file didn't exist
            nothing that we need to do 
            """

        try:
            os.rename(self._path, "{}.backup".format(self._path))
        except FileNotFoundError:
            """
            no-op because file didn't exist
            nothing that we need to do 
            """

        file_handler = self._get_file_handler()
        file_handler.write(contents)
        file_handler.close()

    def _save_store_to_file(self) -> None:
        self._file_content = json.dumps(self._store)

    def _load_store_from_file(self) -> None:
        contents = self._file_content
        if contents is None or len(contents) == 0:
            self._store = {}
            return None

        try:
            self._store = json.loads(contents)
        except json.decoder.JSONDecodeError:
            """
            error parsing contents as json
            """
            print("Error parsing contents {}: {}".format(self._path, contents))
            self._store = {}

    def __getattr__(self, key):
        if key in self._class_attributes:
            return None
        if key not in self._store.keys():
            return None
        return self._store[key]

    def __setattr__(self, key, value):
        if key in self._class_attributes:
            return object.__setattr__(self, key, value)

        if self._store is None:
            self._store = {}
        self._store.update({key: value})
        self._save_store_to_file()



deviceConfig = ConfigHandler("/config/device.json")
displayConfig = ConfigHandler("/config/display.json")
mqttConfig = ConfigHandler("/config/mqtt.json")
