from ...connection_hub import ConnectionHub
from .property import Property


class Service:
    props: dict[str, Property] = {}

    def __init__(self, connection_hub: ConnectionHub):
        self.hub = connection_hub
        self.registered = False

    def add_property(self, key: str, prop: Property):
        self.props[key] = prop

    def get_properties(self):
        return self.props

    def get_property(self, key: str):
        return self.props[key]

    def register(self):
        for prop in self.props.values():
            prop.register()
        self.registered = True

    def sync(self):
        for prop in self.props.values():
            prop.pull()
