#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Version:  # pylint: disable=[R0903]
    """Print the version."""

    def __init__(self) -> None:
        self.version = '5.2.1'
        self.license = 'GNU General Public License v3 (GPLv3)'
        self.author = 'dslackw'
        self.homepage = 'https://dslackw.gitlab.io/slpkg'
        self.email = 'dslackw@gmail.com'

    def view(self) -> None:
        """Print the version."""
        print(f'Version: {self.version}\n'
              f'Author: {self.author}\n'
              f'License: {self.license}\n'
              f'Homepage: {self.homepage}\n'
              f'Email: {self.email}')
