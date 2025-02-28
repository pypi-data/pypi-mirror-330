import json
import pprint


class Payload:

    def __init__(self, data: dict):
        self.data = data


    def format(self):
        formatted : dict = {}
        for key, value in self.data.items():
            if isinstance(value, dict):
                formatted[key] = json.dumps(value)
            else:
                formatted[key] = value
        return formatted

    def __str__(self):
        return f'Payload\ndata = {pprint.pformat(self.data)}'

    def __repr__(self):
        return f'Payload(data = {pprint.pformat(self.data)} )'