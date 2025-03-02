# -*- coding: UTF-8 -*-
import sys

import base1x

base1x.redirect('trader1x', __file__)

from trader1x.auto import auto_trader


if __name__ == '__main__':
    sys.exit(auto_trader())
