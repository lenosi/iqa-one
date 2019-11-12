from iqa.components.abstract.component import Component
from iqa.components.abstract.configuration import Configuration


class RouterConfiguration(Configuration):

    def __init__(self, component: Component, **kwargs) -> None:
        super(RouterConfiguration, self).__init__(component, **kwargs)

    def apply_config(self, configuration: Configuration) -> None:
        pass

    def create_default_configuration(self, **kwargs) -> None:
        pass

    def create_configuration(self, config_file_path: str) -> None:
        self.load_configuration_yaml(config_file_path)

    def load_configuration(self) -> None:
        pass
