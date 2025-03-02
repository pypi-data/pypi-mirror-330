from .argument import Argument

class Block:
    """
    A code block.
    """

    def __init__(self, action: str, arguments: list[Argument], body: list['Block'] = None):
        """
        Creates a new Block of a template.
        :param action: The action to execute
        :param arguments: The arguments the block takes
        :param body: The body of the block for ifs and repeats and the like. Defaults to ``None``.
        """
        self.action = action
        self.arguments = arguments
        self.body = body

    def __repr__(self):
        return f"Block({self.action!r}, {self.arguments!r}, {self.body!r})"

    def __iadd__(self, other):
        if isinstance(other, Block):
            if not self.body:
                self.body = []
            self.body.append(other)
        elif isinstance(other, list):
            if not self.body:
                self.body = []
            self.body.extend(other)
        elif isinstance(other, Argument):
            self.arguments.append(other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +=: 'Block' and '{other.__class__.__name__}'"
            )

    @classmethod
    def from_json(cls, json: dict) -> 'Block':
        action = json["action"]
        arguments = [Argument.from_json(arg) for arg in json["values"]]
        body = [Block.from_json(block) for block in json.get("operations", [])]
        return cls(action, arguments, body)

    def to_json(self) -> dict:
        data = {
            "action": self.action,
            "values": [value.to_json() for value in self.arguments]
        }
        if self.body:
            data["operations"] = [block.to_json() for block in self.body]

        return data
