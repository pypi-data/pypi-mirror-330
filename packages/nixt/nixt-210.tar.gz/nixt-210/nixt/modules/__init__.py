# This file is placed in the Public Domain.
# ruff: noqa: F401


"interface"


import importlib
import os
import time


STARTTIME = time.time()
IGNORE    = ["llm.py", "mbx.py", "rst.py", "web.py", "wsd.py", "udp.py"]
MODS      = sorted([
                    x[:-3] for x in os.listdir(os.path.dirname(__file__))
                    if x.endswith(".py") and not x.startswith("__")
                    and x not in IGNORE
                   ])


def __dir__():
    return MODS
