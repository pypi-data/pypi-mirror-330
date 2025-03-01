#!/usr/bin/python3
# -*- coding: utf-8 -*-


from pathlib import Path

import tomlkit
from slpkg.configs import Configs
from slpkg.toml_errors import TomlErrors
from tomlkit import exceptions


class Blacklist(Configs):  # pylint: disable=[R0903]
    """Reads and returns the blacklist."""

    def __init__(self) -> None:
        super().__init__()

        self.toml_errors = TomlErrors()
        self.blacklist_file_toml: Path = Path(self.etc_path, 'blacklist.toml')

    def packages(self) -> list[str]:
        """Read the blacklist file.

        Returns:
            list[str]: Name of packages.
        """
        packages: list[str] = []
        if self.blacklist_file_toml.is_file():
            try:
                with open(self.blacklist_file_toml, 'r', encoding='utf-8') as file:
                    black: dict[str, str] = tomlkit.parse(file.read())
                    packages = black['PACKAGES']   # type: ignore # pyright: ignore[reportAssignmentType]
            except (KeyError, exceptions.TOMLKitError) as error:
                print()
                self.toml_errors.raise_toml_error_message(str(error), self.blacklist_file_toml)

        return packages
