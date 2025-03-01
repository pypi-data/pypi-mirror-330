#!/usr/bin/python3
# -*- coding: utf-8 -*-


from pathlib import Path

from slpkg.configs import Configs
from slpkg.repositories import Repositories
from slpkg.utilities import Utilities


class ViewPackage(Configs):  # pylint: disable=[R0902]
    """View the packages' information."""

    def __init__(self, flags: list[str], repository: str) -> None:
        super().__init__()

        self.flags = flags
        self.repository = repository

        self.utils = Utilities()
        self.repos = Repositories()

        self.repository_packages: tuple[str, ...] = ()
        self.readme: list[str] = []
        self.info_file: list[str] = []
        self.repo_build_tag: str = ''
        self.mirror: str = ''
        self.homepage: str = ''
        self.maintainer: str = ''
        self.email: str = ''
        self.dependencies: str = ''
        self.repo_tar_suffix: str = ''

        self.option_for_pkg_version: bool = self.utils.is_option(
            ('-p', '--pkg-version'), flags)

    def slackbuild(self, data: dict[str, dict[str, str]], slackbuilds: list[str]) -> None:
        """View slackbuilds information.

        Args:
            data (dict[str, dict[str, str]]): Repository data.
            slackbuilds (list[str]): List of slackbuilds.
        """
        print()
        repo: dict[str, str] = {
            self.repos.sbo_repo_name: self.repos.sbo_repo_tar_suffix,
            self.repos.ponce_repo_name: ''
        }
        git_mirror: dict[str, str] = {
            self.repos.sbo_repo_name: self.repos.sbo_git_mirror,
            self.repos.ponce_repo_name: self.repos.ponce_git_mirror
        }

        self.repo_tar_suffix = repo[self.repository]

        self.mirror = self.repos.repositories[self.repository]['mirror_packages']
        if '.git' in git_mirror[self.repository]:
            repo_path = self.utils.get_git_branch(self.repos.repositories[self.repository]['path'])
            self.mirror = git_mirror[self.repository].replace('.git', f'/tree/{repo_path}/')
            self.repo_tar_suffix = '/'

        self.repository_packages = tuple(data.keys())

        for sbo in slackbuilds:
            for name, item in data.items():

                if sbo in [name, '*']:
                    path_file: Path = Path(self.repos.repositories[self.repository]['path'],
                                           item['location'], name, 'README')
                    path_info: Path = Path(self.repos.repositories[self.repository]['path'],
                                           item['location'], name, f'{name}.info')

                    self.read_the_readme_file(path_file)
                    self.read_the_info_file(path_info)
                    self.repo_build_tag = data[name]['build']
                    self.assign_the_info_file_variables()
                    self.assign_dependencies(item)
                    self.assign_dependencies_with_version(item, data)
                    self.view_slackbuild_package(name, item)

    def read_the_readme_file(self, path_file: Path) -> None:
        """Read the README file.

        Args:
            path_file (Path): Path to the file.
        """
        self.readme = self.utils.read_text_file(path_file)

    def read_the_info_file(self, path_info: Path) -> None:
        """Read the .info file.

        Args:
            path_info (Path): Path to the file.
        """
        self.info_file = self.utils.read_text_file(path_info)

    def assign_the_info_file_variables(self) -> None:
        """Assign data from the .info file."""
        for line in self.info_file:
            if line.startswith('HOMEPAGE'):
                self.homepage = line[10:-2].strip()
            if line.startswith('MAINTAINER'):
                self.maintainer = line[12:-2].strip()
            if line.startswith('EMAIL'):
                self.email = line[7:-2].strip()

    def assign_dependencies(self, item: dict[str, str]) -> None:
        """Assign the package dependencies.

        Args:
            item (dict[str, str]): Data value.
        """
        self.dependencies = ', '.join([f'{self.cyan}{pkg}' for pkg in item['requires']])

    def assign_dependencies_with_version(self, item: dict[str, str], data: dict[str, dict[str, str]]) -> None:
        """Assign dependencies with version.

        Args:
            item (dict[str, str]): Data value.
            data (dict[str, dict[str, str]]): Repository data.
        """
        if self.option_for_pkg_version:
            self.dependencies = (', '.join(
                [f"{self.cyan}{pkg}{self.endc}-{self.yellow}{data[pkg]['version']}"
                 f"{self.green}" for pkg in item['requires']
                 if pkg in self.repository_packages]))

    def view_slackbuild_package(self, name: str, item: dict[str, str]) -> None:
        """Print slackbuild information.

        Args:
            name (str): Slackbuild name.
            item (dict[str, str]): Data value.
        """
        space_align: str = ''
        print(f"{'Repository':<15}: {self.green}{self.repository}{self.endc}\n"
              f"{'Name':<15}: {self.green}{name}{self.endc}\n"
              f"{'Version':<15}: {self.green}{item['version']}{self.endc}\n"
              f"{'Build':<15}: {self.green}{self.repo_build_tag}{self.endc}\n"
              f"{'Homepage':<15}: {self.blue}{self.homepage}{self.endc}\n"
              f"{'Download SBo':<15}: {self.blue}{self.mirror}"
              f"{item['location']}/{name}{self.repo_tar_suffix}{self.endc}\n"
              f"{'Sources':<15}: {self.blue}{' '.join(item['download'])}{self.endc}\n"
              f"{'Md5sum':<15}: {self.yellow}{' '.join(item['md5sum'])}{self.endc}\n"
              f"{'Sources x86_64':<15}: {self.blue}{' '.join(item['download64'])}{self.endc}\n"
              f"{'Md5sum x86_64':<15}: {self.yellow}{' '.join(item['md5sum64'])}{self.endc}\n"
              f"{'Files':<15}: {self.green}{' '.join(item['files'])}{self.endc}\n"
              f"{'Category':<15}: {self.red}{item['location']}{self.endc}\n"
              f"{'SBo url':<15}: {self.blue}{self.mirror}{item['location']}/{name}/{self.endc}\n"
              f"{'Maintainer':<15}: {self.yellow}{self.maintainer}{self.endc}\n"
              f"{'Email':<15}: {self.yellow}{self.email}{self.endc}\n"
              f"{'Requires':<15}: {self.green}{self.dependencies}{self.endc}\n"
              f"{'Description':<15}: {self.green}{item['description']}{self.endc}\n"
              f"{'README':<15}: {self.cyan}{f'{space_align:>17}'.join(self.readme)}{self.endc}")

    def package(self, data: dict[str, dict[str, str]], packages: list[str]) -> None:
        """View binary packages information.

        Args:
            data (dict[str, dict[str, str]]): Repository data.
            packages (list[str]): List of packages.
        """
        print()
        self.repository_packages = tuple(data.keys())
        for package in packages:
            for name, item in data.items():
                if package in [name, '*']:

                    self.assign_dependencies(item)
                    self.assign_dependencies_with_version(item, data)
                    self.view_binary_package(name, item)

    def view_binary_package(self, name: str, item: dict[str, str]) -> None:
        """Print binary packages information.

        Args:
            name (str): Package name.
            item (dict[str, str]): Data values.
        """
        print(f"{'Repository':<15}: {self.green}{self.repository}{self.endc}\n"
              f"{'Name':<15}: {self.green}{name}{self.endc}\n"
              f"{'Version':<15}: {self.green}{item['version']}{self.endc}\n"
              f"{'Build':<15}: {self.green}{item['build']}{self.endc}\n"
              f"{'Package':<15}: {self.cyan}{item['package']}{self.endc}\n"
              f"{'Download':<15}: {self.blue}{item['mirror']}{item['location']}/{item['package']}{self.endc}\n"
              f"{'Md5sum':<15}: {item['checksum']}\n"
              f"{'Mirror':<15}: {self.blue}{item['mirror']}{self.endc}\n"
              f"{'Location':<15}: {self.red}{item['location']}{self.endc}\n"
              f"{'Size Comp':<15}: {self.yellow}{item['size_comp']} KB{self.endc}\n"
              f"{'Size Uncomp':<15}: {self.yellow}{item['size_uncomp']} KB{self.endc}\n"
              f"{'Requires':<15}: {self.green}{self.dependencies}{self.endc}\n"
              f"{'Conflicts':<15}: {item['conflicts']}\n"
              f"{'Suggests':<15}: {item['suggests']}\n"
              f"{'Description':<15}: {item['description']}\n")
