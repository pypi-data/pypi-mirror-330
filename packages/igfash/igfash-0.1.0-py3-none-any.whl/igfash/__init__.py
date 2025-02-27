#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

__all__ = [
    "io",
    "compute",
    "window",
]

# use date and time as the version number    
# import datetime
# __version__ = datetime.datetime.now().strftime('%Y.%m.%d.%H%M')

# use github release tag as the version number
import os
try:
    __version__ = os.environ["GITHUB_REF_NAME"]
except:
    __version__ = "0.1.0"