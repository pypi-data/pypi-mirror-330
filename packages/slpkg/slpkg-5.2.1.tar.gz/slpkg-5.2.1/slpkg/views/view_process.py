#!/usr/bin/python3
# -*- coding: utf-8 -*-


import time
from multiprocessing import Process
from typing import Optional

from slpkg.configs import Configs
from slpkg.progress_bar import ProgressBar
from slpkg.utilities import Utilities
from slpkg.views.asciibox import AsciiBox


class ViewProcess(Configs):
    """View the process messages."""

    def __init__(self) -> None:
        super().__init__()

        self.progress = ProgressBar()
        self.utils = Utilities()
        self.ascii = AsciiBox()

        self.bar_process: Optional[Process] = None

    def message(self, message: str) -> None:
        """Show spinner with message.

        Args:
            message (str): Message of spinner.
        """
        self.bar_process = Process(target=self.progress.progress_bar, args=(message,))
        self.bar_process.start()

    def done(self) -> None:
        """Show done message."""
        time.sleep(0.1)
        if self.bar_process is not None:
            self.bar_process.terminate()
            self.bar_process.join()
        print(f'\b{self.bgreen}{self.ascii.done}{self.endc}', end='')
        print('\x1b[?25h')  # Reset cursor after hiding.

    def failed(self) -> None:
        """Show for failed message."""
        time.sleep(0.1)
        if self.bar_process is not None:
            self.bar_process.terminate()
            self.bar_process.join()
        print(f'\b{self.bred}{self.ascii.failed}{self.endc}', end='')
        print('\x1b[?25h')  # Reset cursor after hiding.
