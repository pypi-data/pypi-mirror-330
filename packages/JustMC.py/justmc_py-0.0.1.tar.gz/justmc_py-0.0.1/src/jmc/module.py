import requests
from .template import Template

class Module:
    """
    A JustMC Module, can store multiple Templates.
    """
    def __init__(self, templates: list[Template]):
        """
        Creates a Module.
        :param templates: List of templates
        """
        self.templates = templates

    @classmethod
    def from_json(cls, data: dict) -> 'Module':
        """
        Gets a Module from a Module JSON.
        :param data: The JSON as a dictionary
        :return: The parsed Module.
        """
        return cls([Template.from_json(template) for template in data["handlers"]])

    def to_json(self) -> dict:
        """
        Converts the Module to its JSON representation.
        :return: The JSON representation
        """
        handlers = []
        for i, template in enumerate(self.templates):
            handlers.append(template.to_json(i))

        return {
            "handlers": handlers
        }

    def __repr__(self):
        return f"Module({self.templates!r})"

    def upload(self) -> str:
        """
        **This is a synchronous operation.**

        Uploads the module onto the JustMC servers. The module then can be loaded via the ``/module loadUrl force? <url>`` command.
        :return: The URL to load from
        """
        response = requests.post("https://m.justmc.ru/api/upload", json=self.to_json()).json()
        return f"https://m.justmc.ru/api/{response['id']}"
