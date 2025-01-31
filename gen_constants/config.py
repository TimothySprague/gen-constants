from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class ConstantDefinition(object):
    name: Optional[str] = field(init=False, default=None)
    value: Optional[Any] = field(init=False, default=None)

    def add(self, name: str, value: Any) -> None:
        assert self.name is None
        assert self.value is None

        self.name = name
        self.value = value


@dataclass
class EnumConstant(object):
    values: dict[str, int] = field(init=False, default_factory=dict)

    def add(self, key: str, value: str) -> None:
        assert key not in self.values
        # TODO: Validate that value is a non-negative integer type
        self.values[key] = int(value, 0)


@dataclass
class Constants(object):
    constants: list[ConstantDefinition] = field(init=False, default_factory=list)
    anonymous_enums: list[EnumConstant] = field(init=False, default_factory=list)
    named_enums: dict[str, EnumConstant] = field(init=False, default_factory=dict)


def parse_config(config_file: Path) -> Constants:
    cp = ConfigParser()
    cp.read(config_file)

    constants = Constants()

    def _is_constants(section_name: str) -> bool:
        return section_name.lower() == 'constants' or section_name.lower().startswith('constants.')

    for section in cp.sections():
        if _is_constants(section):
            # TODO: Anything to do with the section name?
            const_obj = ConstantDefinition()
        elif section.lower().startswith('anonymous_enum.'):
            const_obj = EnumConstant()
            constants.anonymous_enums.append(const_obj)
        elif section.lower().startswith('named_enum.'):
            # TODO: Validate the enum name
            enum_name = section.split('.', maxsplit=1)[1].lower()
            const_obj = EnumConstant()
            assert enum_name not in constants.named_enums
            constants.named_enums[enum_name] = const_obj
        else:
            raise NotImplementedError(f'Section "{section}" not supported')

        for key, value in cp.items(section):
            const_obj.add(key, value)

            if _is_constants(section):
                constants.constants.append(const_obj)
                const_obj = ConstantDefinition()

    return constants
