import os
import re
import yaml
import trafaret as t


class ConfigLoader(yaml.SafeLoader):
    """This is :class:`yaml.SafeLoafer` wrapper to add custom tags.

    Tags functions:
        - include: read yaml file from the same root. Tag: !include
        - read_env: read environment variables. Tag: !ENV
    """

    def __init__(self, stream):
        """Constructor method."""  # noqa: D401
        self._root = os.path.split(stream.name)[0]
        # pattern looks for ${var}
        self.pattern = re.compile('.*?\${(\w+)}.*?')  # noqa: W605
        super(ConfigLoader, self).__init__(stream)

    def include(self, node):
        """Read yaml file from the same root. Tag: !include."""
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, ConfigLoader)

    def read_env(self, node):
        """Read environment variables. Tag: !ENV."""
        value = self.construct_scalar(node)
        match = self.pattern.findall(value)
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value

    @classmethod
    def add_constructors(cls):
        """Add all constructors."""
        cls.add_constructor('!include', cls.include)
        cls.add_constructor('!ENV', cls.read_env)


ConfigLoader.add_constructors()


def get_config(path: str) -> dict:
    """Read config from yaml file and validates it.

    Contains config validator:
        - config dict should contain 'postgres' 'app' keys
        - extra keys are allowed

    :param path: path to config file
    :raises ValueError: if config object is not valid
    :returns: config object(dict)
    """
    config_validator = t.Dict(
        {
            'postgres': t.Dict(allow_extra=['*']),
            'app': t.Dict(allow_extra=['*'])
        },
        allow_extra=['*']
    )

    with open(path, 'r') as f:
        try:
            config = yaml.load(f, ConfigLoader)
            config_validator.check(config)
            return config
        except t.DataError as e:
            raise ValueError(f'Config is not valid: {e.as_dict()}') from e
