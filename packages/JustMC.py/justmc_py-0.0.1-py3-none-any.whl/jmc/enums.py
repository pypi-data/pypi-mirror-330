from enum import Enum
import json

class TextParsing(Enum):
    LEGACY = "legacy"
    MINIMESSAGE = "minimessage"
    JSON = "json"
    PLAIN = "plain"

class Scope(Enum):
    LOCAL = "local"
    SAVED = "save"
    GAME = "game"

class Selection(Enum):
    NONE = "null"
    CURRENT = "current"
    DEFAULT = "default"
    DEFAULT_ENTITY = "default_entity"
    KILLER = "killer_entity"
    DAMAGER = "damager_entity"
    VICTIM = "victim_entity"
    SHOOTER = "shooter_entity"
    PROJECTILE = "projectile"
    LAST_ENTITY = "last_entity"

    @classmethod
    def from_value(cls, selection: str) -> 'Selection':
        """
        Gets the Selection value from the selection KV pair in the internal JSON.
        :param selection: The selection value
        :return: The parsed Selection object
        """
        if selection == "null": return cls.NONE
        return cls(json.loads(selection)["type"])

    def to_value(self) -> str:
        """
        Gets the internal JSON value for the selection.
        :return: The serialized selection value
        """
        if self == Selection.NONE: return "null"
        return json.dumps({"type": self.value})

class SoundSource(Enum):
    MASTER = "MASTER"
    AMBIENT = "AMBIENT"
    BLOCK = "BLOCK"
    HOSTILE = "HOSTILE"
    MUSIC = "MUSIC"
    NEUTRAL = "NEUTRAL"
    PLAYER = "PLAYER"
    RECORD = "RECORD"
    VOICE = "VOICE"
    WEATHER = "WEATHER"