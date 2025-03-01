#!/usr/bin/python3
# -*- coding: utf-8 -*-


from typing import cast

from slpkg.utilities import Utilities


class Requires:
    """Create a tuple with package dependencies."""

    __slots__ = (
        'data', 'name', 'flags', 'utils', 'option_for_resolve_off'
    )

    def __init__(self, data: dict[str, dict[str, str]], name: str, flags: list[str]) -> None:
        self.data = data
        self.name = name
        self.utils = Utilities()

        self.option_for_resolve_off: bool = self.utils.is_option(
            ('-O', '--resolve-off'), flags)

    def resolve(self) -> tuple:
        """Resolve the dependencies.

        Return package dependencies in the right order.
        """
        dependencies: tuple[str, ...] = ()

        if not self.option_for_resolve_off:
            requires: list[str] = self.remove_deps(cast(list[str], self.data[self.name]['requires']))

            for require in requires:
                sub_requires: list[str] = self.remove_deps(cast(list[str], self.data[require]['requires']))

                for sub in sub_requires:
                    requires.append(sub)

            requires.reverse()
            dependencies = tuple(dict.fromkeys(requires))

        return dependencies

    def remove_deps(self, requires: list[str]) -> list:
        """Remove requirements that not in the repository.

        Args:
            requires (list[str]): List of requires.

        Returns:
            list: List of packages name.
        """
        return [req for req in requires if req in self.data]
