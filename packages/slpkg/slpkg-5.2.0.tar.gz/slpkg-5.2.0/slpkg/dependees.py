#!/usr/bin/python3
# -*- coding: utf-8 -*-


from typing import Generator

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.asciibox import AsciiBox


class Dependees(Configs):  # pylint: disable=[R0902]
    """Prints the packages that depend on."""

    def __init__(self, data: dict[str, dict[str, str]], packages: list[str], flags: list[str]) -> None:
        super().__init__()
        self.data = data
        self.packages = packages
        self.flags = flags

        self.ascii = AsciiBox()
        self.utils = Utilities()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.var: str = self.ascii.vertical_and_right
        self.package_version: str = ''

        self.option_for_full_reverse: bool = self.utils.is_option(
            ('-E', '--full-reverse'), flags)

        self.option_for_pkg_version: bool = self.utils.is_option(
            ('-p', '--pkg-version'), flags)

    def find(self) -> None:
        """Call the methods."""
        print('The list below shows the packages that dependees on:\n')
        self.packages = self.utils.apply_package_pattern(self.data, self.packages)

        for package in self.packages:
            dependees: dict = dict(self.find_requires(package))
            self.view_the_main_package(package)
            self.view_no_dependees(dependees)
            self.view_dependees(dependees)
            self.view_summary_of_dependees(dependees, package)

    def set_the_package_version(self, package: str) -> None:
        """Set the version of the package.

        Args:
            package (str): Package name.
        """
        self.package_version = self.data[package]['version']

    def find_requires(self, package: str) -> Generator:
        """Find requires that package dependees.

        Args:
            package (str): Package name.

        Yields:
            Generator: List of names with requires.
        """
        for name, data in self.data.items():
            if package in data['requires']:
                yield name, data['requires']

    def view_no_dependees(self, dependees: dict[str, str]) -> None:
        """Print for no dependees.

        Args:
            dependees (dict[str, str]): Packages data.
        """
        if not dependees:
            print(f"{'':>1}{self.cyan}No dependees{self.endc}")

    def view_the_main_package(self, package: str) -> None:
        """Print the main package.

        Args:
            package (str): Package name.
        """
        print(f'{self.byellow}{package}{self.endc}')
        print(f"{'':>1}{self.llc}{self.hl}", end='')

    @staticmethod
    def view_dependency_line(n: int, dependency: str) -> None:
        """Print the dependency line.

        Args:
            n (int): Line number.
            dependency (str): Name of dependency.
        """
        str_dependency: str = f"{'':>4}{dependency}"
        if n == 1:
            str_dependency = f"{'':>1}{dependency}"
        print(str_dependency)

    def view_dependees(self, dependees: dict[str, str]) -> None:
        """View packages that depend on.

        Args:
            dependees (dict): Packages data.
        """
        name_length: int = 0
        if dependees:
            name_length = max(len(name) for name in dependees.keys())
        for n, (name, requires) in enumerate(dependees.items(), start=1):
            dependency: str = f'{self.cyan}{name}{self.endc}'
            if self.option_for_pkg_version:
                self.set_the_package_version(name)
                dependency = (f'{self.cyan}{name:<{name_length}}{self.endc} {self.yellow}'
                              f'{self.package_version}{self.endc}')

            self.view_dependency_line(n, dependency)

            if self.option_for_full_reverse:
                self.view_full_reverse(n, dependees, requires)

    def view_full_reverse(self, n: int, dependees: dict[str, str], requires: str) -> None:
        """Print all packages.

        Args:
            n (int): Number of line.
            dependees (dict[str, str]): Packages data.
            requires (str): Package requires.
        """
        line_requires: str = f"{'':>5}{self.var}{self.hl} {self.violet}{','.join(requires)}{self.endc}"
        if n == len(dependees):
            line_requires = f"{'':>5}{self.llc}{self.hl} {self.violet}{','.join(requires)}{self.endc}"
        print(line_requires)

    def view_summary_of_dependees(self, dependees: dict[str, str], package: str) -> None:
        """Print the summary.

        Args:
            dependees (dict[str, str]): Packages data.
            package (str): Package name.
        """
        print(f'\n{self.grey}{len(dependees)} dependees for {package}{self.endc}\n')
