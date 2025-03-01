#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

if not os.geteuid() == 0:
    sys.exit('Must run as root.')

from slpkg.main import main  # pylint: disable=[C0413]

if __name__ == "__main__":
    main()
