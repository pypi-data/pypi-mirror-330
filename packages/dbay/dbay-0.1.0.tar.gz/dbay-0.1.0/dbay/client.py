from dbay.modules.dac4d import dac4D
from dbay.modules.dac16d import dac16D
from dbay.modules.empty import Empty
from dbay.http import Http
import time
from typing import List, Union


class DBay:
    def __init__(self, server_address: str, port: int = 8345):
        self.server_address = server_address
        self.port = port
        self.modules: List[Union[dac4D, dac16D, Empty]] = [None] * 8
        self.http = Http(server_address, port)
        self.load_full_state()

    def load_full_state(self):
        response = self.http.get("full-state")
        self.instantiate_modules(response["data"])

    def instantiate_modules(self, module_data: list):
        for i, module_info in enumerate(module_data):
            module_type = module_info["core"]["type"]
            if module_type == "dac4D":
                # print("info about dac4D class:"
                self.modules[i] = dac4D(module_info, self.http)
            elif module_type == "dac16D":
                self.modules[i] = dac16D(module_info, self.http)
            else:
                self.modules[i] = Empty()

    def get_modules(self):
        return self.modules

    # Additional methods to interact with the modules can be added here.
