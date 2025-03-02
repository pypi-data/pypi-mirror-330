from .argument import Argument

class Header:
    """
    A structure indicating a code starter or header.
    """
    type: str

    @classmethod
    def from_json(cls, json: dict) -> 'Header':
        type = json["type"]
        if type == "event":
            return Event.from_json(json)
        elif type == "function":
            return Function.from_json(json)
        elif type == "process":
            return Process.from_json(json)

    def to_json(self) -> dict:
        """
        Converts the Header into a dictionary.
        :return: The dictionary
        """
        pass

class Event(Header):
    """
    A Player, Entity, or World event.
    """
    type = "event"

    def __init__(self, event: str):
        """
        Creates a new Event header.
        :param event: The event that will trigger
        """
        self.event = event

    def __repr__(self):
        return f"Event({self.event!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Event':
        return cls(json["event"])

    def to_json(self) -> dict:
        return {
            "type": "event",
            "event": self.event
        }

class Function(Header):
    """
    A named Function.
    """
    type = "function"

    def __init__(self, name: str, values: list[Argument]):
        """
        Creates a new Function header type.
        :param name: The name of the function
        :param values: The arguments to take
        """
        self.name = name
        self.values = values

    def __repr__(self):
        return f"Function({self.name!r}, {self.values!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Function':
        return cls(json["name"], json["values"])

    def to_json(self) -> dict:
        return {
            "type": "function",
            "name": self.name,
            "values": [value.to_json() for value in self.values]
        }


class Process(Header):
    """
    A named Process.
    """
    type = "process"

    def __init__(self, name: str, values: list[Argument]):
        """
        Creates a new Process header type.
        :param name: The name of the process
        :param values: The arguments to take
        """
        self.name = name
        self.values = values

    def __repr__(self):
        return f"Process({self.name!r}, {self.values!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Process':
        return cls(json["name"], json["values"])

    def to_json(self) -> dict:
        return {
            "type": "process",
            "name": self.name,
            "values": [value.to_json() for value in self.values]
        }