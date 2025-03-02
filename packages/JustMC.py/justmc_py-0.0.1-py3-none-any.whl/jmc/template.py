import json
import base64
import zlib
from .block import Block
from .headers import Header

class Template:
    """
    A JustMC code template.
    """
    def __init__(self, header: Header, blocks: list[Block]):
        """
        Creates a new code Template.
        :param header: The header that will start the execution
        :param blocks: The code of the template
        """
        self.header = header
        self.blocks = blocks

    def __repr__(self):
        return f"Template({self.header!r}, {self.blocks!r})"

    def __iadd__(self, other):
        if isinstance(other, list):
            self.blocks.extend(other)
        elif isinstance(other, Block):
            self.blocks.append(other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +=: 'Template' and '{other.__class__.__name__}'"
            )

    @classmethod
    def from_json(cls, json: dict) -> 'Template':
        """
        Gets a Template object from the loaded JSON.
        :param json: JSON loaded as a dictionary
        :return: The parsed Template object
        """
        header_type = Header.from_json(json)
        blocks = [Block.from_json(block) for block in json["operations"]]
        return cls(header_type, blocks)

    def to_json(self, position: int = 0) -> dict:
        """
        Converts the Template into a JSON dictionary.
        :param position: The position of the Template in a module
        :return: The JSON dictionary
        """
        data = self.header.to_json()
        data["operations"] = [block.to_json() for block in self.blocks]
        data["position"] = position
        return data

    @classmethod
    def decompress(cls, data: str) -> 'Template':
        """
        Gets a Template object from the compressed data string.
        :param data: Base64 encoded data string
        :return: The decompressed Template object
        """
        return cls.from_json(json.loads(zlib.decompress(base64.b64decode(data.encode())).decode()))

    def compress(self) -> str:
        """
        Compresses the Template object back into a data string.
        :return: The compressed Template string
        """
        return base64.b64encode(zlib.compress(json.dumps(self.to_json()).encode())).decode()
