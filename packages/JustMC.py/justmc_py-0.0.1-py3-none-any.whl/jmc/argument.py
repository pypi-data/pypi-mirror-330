from .enums import TextParsing, Scope, Selection, SoundSource
from amulet_nbt import CompoundTag, load as amulet_nbt_load, StringTag, IntTag
import base64


class ValueItem:
    """
    A value item used in Argument.
    """

    @classmethod
    def from_json(cls, json: dict) -> 'ValueItem':
        """
        Gets a ValueItem from an item JSON.
        :param json: The JSON as a dictionary
        :return: The parsed ValueItem
        """
        if not json: return NullValue()

        type = json["type"]
        if type == "array":
            return PluralArgument.from_json(json)
        elif type == "text":
            return Text.from_json(json)
        elif type == "number":
            return Number.from_json(json)
        elif type == "location":
            return Location.from_json(json)
        elif type == "variable":
            return Variable.from_json(json)
        elif type == "game_value":
            return GameValue.from_json(json)
        elif type == "vector":
            return Vector.from_json(json)
        elif type == "sound":
            return Sound.from_json(json)
        elif type == "particle":
            return Particle.from_json(json)
        elif type == "potion":
            return Potion.from_json(json)
        elif type == "item":
            return Item.from_json(json)
        elif type == "enum":
            return Enum.from_json(json)
    
    def to_json(self) -> dict:
        """
        Converts the Valueitem to a dictionary.
        :return: The dictionary
        """
        pass


class NullValue(ValueItem):
    """
    A nothing value for empty slots.
    """

    def __repr__(self):
        return f"NullValue()"
    
    def to_json(self) -> dict:
        return {}


class PluralArgument(ValueItem):
    """
    An argument representing parameters that takes in more than one values.
    """

    def __init__(self, values: list[ValueItem]):
        """
        Creates a new PluralArgument with the following values.
        :param values: The list of values to pass in
        """
        self.values = values

    def __iadd__(self, other):
        if isinstance(other, ValueItem):
            self.values.append(other)
        elif isinstance(other, list):
            self.values.extend(other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +=: 'Block' and '{other.__class__.__name__}'"
            )

    def __repr__(self):
        return f"PluralArgument({self.values!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'PluralArgument':
        return cls([ValueItem.from_json(item) for item in json["values"]])
    
    def to_json(self) -> dict:
        return {
            "type": "array",
            "values": [
                value.to_json() for value in self.values
            ]
        }


class Text(ValueItem):
    """
    A value representing a Text.
    """

    def __init__(self, text: str, parsing: TextParsing = TextParsing.MINIMESSAGE):
        """
        Creates a new Text argument value.
        :param text: The text to take
        :param parsing: The style parsing of the text. Defaults to ``TextParsing.MINIMESSAGE``.
        """
        self.text = text
        self.parsing = parsing

    def __repr__(self):
        return f"Text({self.text!r}, {self.parsing.name})"

    @classmethod
    def from_json(cls, json: dict) -> 'Text':
        return cls(json["text"], TextParsing(json["parsing"]))

    def to_json(self) -> dict:
        return {
            "type": "text",
            "text": self.text,
            "parsing": self.parsing.value
        }


class Number(ValueItem):
    """
    A value representing a Number.
    """

    def __init__(self, number: float | int | str):
        """
        Creates a new Number argument value.
        :param number: The number to take
        """
        self.number = number

    def __repr__(self):
        return f"Number({self.number!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Number':
        return cls(json["number"])

    def to_json(self) -> dict:
        return {
            "type": "number",
            "number": self.number
        }


class Location(ValueItem):
    """
    A value representing a Location.
    """

    def __init__(self, x: float, y: float, z: float, yaw: float = 0, pitch: float = 0):
        """
        Creates a new Location argument value.
        :param x: The X position
        :param y: The Y position
        :param z: The Z position
        :param yaw: The yaw rotation (left-right)
        :param pitch: The pitch rotation (up-down)
        """
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

    def __repr__(self):
        return f"Location({self.x!r}, {self.y!r}, {self.z!r}, {self.yaw!r}, {self.pitch!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Location':
        return cls(json["x"], json["y"], json["z"], json["yaw"], json["pitch"])

    def to_json(self) -> dict:
        return {
            "type": "location",
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "yaw": self.yaw,
            "pitch": self.pitch
        }


class Variable(ValueItem):
    """
    A value representing a Variable.
    """

    def __init__(self, name: str, scope: Scope = Scope.LOCAL):
        """
        Creates a new Variable argument value.
        :param name: The name of the variable
        :param scope: The scope of the variable. Defaults to ``Scope.LOCAL``.
        """
        self.name = name
        self.scope = scope

    def __repr__(self):
        return f"Variable({self.name!r}, {self.scope.name})"

    @classmethod
    def from_json(cls, json: dict) -> 'Variable':
        return cls(json["variable"], Scope(json["scope"]))

    def to_json(self) -> dict:
        return {
            "type": "variable",
            "variable": self.name,
            "scope": self.scope.value
        }


class GameValue(ValueItem):
    """
    A value representing a Game Value.
    """

    def __init__(self, value: str, selection: Selection = Selection.DEFAULT):
        """
        Creates a new GameValue argument value.
        :param value: The value to take
        :param selection: The selection of the value. Defaults to ``Selection.DEFAULT``.
        """
        self.value = value
        self.selection = selection

    def __repr__(self):
        return f"GameValue({self.value!r}, {self.selection.name})"

    @classmethod
    def from_json(cls, json: dict) -> 'GameValue':
        return cls(json["game_value"], Selection.from_value(json["selection"]))

    def to_json(self) -> dict:
        return {
            "type": "game_value",
            "game_value": self.value,
            "selection": self.selection.to_value()
        }


class Vector(ValueItem):
    """
    A value representing a Vector.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Creates a new Vector argument value.
        :param x: The X component
        :param y: The Y component
        :param z: The Z component
        """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r}, {self.z!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Vector':
        return cls(json["x"], json["y"], json["z"])

    def to_json(self) -> dict:
        return {
            "type": "vector",
            "x": self.x,
            "y": self.y,
            "z": self.z
        }


class Sound(ValueItem):
    """
    A value representing a Sound.
    """

    def __init__(self, sound: str, pitch: float, volume: float, variation: str = "", source: SoundSource = SoundSource.MASTER):
        """
        Creates a new Sound argument value.
        :param sound: The sound to take as a resource location
        :param pitch: The pitch of the sound, from 0.5 to 2.0
        :param volume: The volume of the sound, from 0.0 to 2.0
        :param variation: The variation of the sound. Defaults to ``""``.
        :param source: The source of the sound. Defaults to ``SoundSource.MASTER``.
        """
        self.sound = sound
        self.pitch = pitch
        self.volume = volume
        self.variation = variation
        self.source = source

    def __repr__(self):
        return f"Sound({self.sound!r}, {self.pitch!r}, {self.volume!r}, {self.variation!r}, {self.source.name})"

    @classmethod
    def from_json(cls, json: dict) -> 'Sound':
        return cls(json["sound"], json["pitch"], json["volume"], json["variation"], SoundSource(json["source"]))

    def to_json(self) -> dict:
        return {
            "type": "sound",
            "sound": self.sound,
            "pitch": self.pitch,
            "volume": self.volume,
            "variation": self.variation,
            "source": self.source.value
        }


class ParticleData:
    """
    Additional data regarding Particles.
    """
    def __init__(self, /,
                 motion: tuple[float, float, float] = (0, 0, 0),
                 color: int = 0xFFFFFFFF,
                 to_color: int = 0xFFFFFFFF,
                 material: str = "",
                 size: float = 1
                 ):
        """
        Extra information for Particles.
        :param motion: The motion of the particle as a vector
        :param color: The color of the particle as an ARGB hex
        :param to_color: The gradient color of the particle as an ARGB hex
        :param material: The material of the particle, formatted as ``MATERIAL_ID``.
        :param size: The size of the particle
        """
        self.motion = motion
        self.color = color
        self.to_color = to_color
        self.material = material
        self.size = size

    def __repr__(self):
        return f"ParticleData(motion={self.motion!r}, color={self.color!r}, to_color={self.to_color!r}, material={self.material!r}, size={self.size!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'ParticleData':
        data = cls()
        if "x_motion" in json:
            data.motion = (json["x_motion"], json["y_motion"], json["z_motion"])
        if "color" in json:
            data.color = ParticleData.i32_uint(json["color"])
        if "to_color" in json:
            data.to_color = ParticleData.i32_uint(json["to_color"])
        if "material" in json:
            data.material = json["material"]
        if "size" in json:
            data.size = json["size"]
        return data

    def to_json(self) -> dict:
        return {
            "x_motion": self.motion[0],
            "y_motion": self.motion[1],
            "z_motion": self.motion[2],
            "color": ParticleData.uint_i32(self.color),
            "to_color": ParticleData.uint_i32(self.to_color),
            "material": self.material,
            "size": self.size
        }

    @staticmethod
    def i32_uint(i32: int) -> int:
        """
        Converts from a signed 32-bit number to an unsigned number.
        :param i32: The signed 32-bit number
        :return: The unsigned number
        """
        return i32 & 0xFFFFFFFF

    @staticmethod
    def uint_i32(uint: int) -> int:
        """
        Converts from an unsigned number to a signed 32-bit number.
        :param uint: The unsigned number
        :return: The signed 32-bit number
        """
        return uint if uint < (1 << 31) else uint - (1 << 32)


class Particle(ValueItem):
    """
    A value representing a Particle. Please use ``ParticleData`` for additional data for each particle.
    """

    def __init__(self, particle_type: str, amount: int = 1, spread: tuple[float, float] = (0, 0), particle_data: ParticleData = None):
        """
        Creates a new Particle argument value.
        :param particle_type: The type of the particle
        :param amount: The amount of particles on display
        :param spread: The (horizontal, vertical) spread of the spawning particles. Defaults to ``(0, 0)``.
        :param particle_data: Additional particle information
        """
        self.particle_type = particle_type
        self.amount = amount
        self.spread = spread
        self.particle_data = particle_data if particle_data else ParticleData()

    def __repr__(self):
        return f"Particle({self.particle_type!r}, {self.amount!r}, {self.spread!r}, {self.particle_data!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Particle':
        return cls(json["particle_type"], json["count"], (json["first_spread"], json["second_spread"]), ParticleData.from_json(json))

    def to_json(self) -> dict:
        data = {
            "type": "particle",
            "particle_type": self.particle_type,
            "count": self.amount,
            "first_spread": self.spread[0],
            "second_spread": self.spread[1]
        }
        data.update(self.particle_data.to_json())
        return data


class Potion(ValueItem):
    """
    A value representing a Potion.
    """

    def __init__(self, potion: str, amplifier: int = 0, duration: int = -1):
        """
        Creates a new Potion argument value.
        :param potion: The type of potion as a resource location
        :param amplifier: The amplifier of the potion
        :param duration: The duration of the potion. Use ``-1`` for infinite.
        """
        self.potion = potion
        self.amplifier = amplifier
        self.duration = duration

    def __repr__(self):
        return f"Potion({self.potion!r}, {self.amplifier!r}, {self.duration!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Potion':
        return cls(json["potion"], json["amplifier"], json["duration"])

    def to_json(self) -> dict:
        return {
            "type": "potion",
            "potion": self.potion,
            "amplifier": self.amplifier,
            "duration": self.duration
        }


class Item(ValueItem):
    """
    A value representing a Minecraft item.
    """

    def __init__(self, nbt: CompoundTag, is_air: bool = False):
        """
        Creates a new Item argument value.
        :param nbt: The NBT of the item
        :param is_air: If the item is air. Defaults to ``False``.
        """
        self.nbt = nbt
        self.is_air = is_air

    def __repr__(self):
        return f"Item({self.nbt}, {self.is_air!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'ValueItem':
        if json["item"] == "AAAAAAAAAAA=":
            return cls(CompoundTag({"id": StringTag("minecraft:air"), "count": IntTag(1)}), True)

        nbt = amulet_nbt_load(
            base64.b64decode(
                json["item"].encode()
            )
        )
        return cls(nbt.tag)

    def to_json(self) -> dict:
        if self.is_air:
            return {
                "type": "item",
                "item": "AAAAAAAAAAA="
            }
        else:
            return {
                "type": "item",
                "item": base64.b64encode(self.nbt.to_nbt()).decode()
            }


class Enum(ValueItem):
    """
    Represents a Block Marker.
    """

    def __init__(self, value: str):
        """
        Creates a new Block Marker.
        :param value: The value it holds
        """
        self.value = value

    def __repr__(self):
        return f"Enum({self.value!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Enum':
        return cls(json["enum"])

    def to_json(self) -> dict:
        return {
            "type": "enum",
            "value": self.value
        }


class Argument:
    """
    An argument placed into a Block.
    """
    def __init__(self, name: str, value: ValueItem):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Argument({self.name!r}, {self.value!r})"

    @classmethod
    def from_json(cls, json: dict) -> 'Argument':
        return cls(json["name"], ValueItem.from_json(json["value"]))

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "value": self.value.to_json()
        }
