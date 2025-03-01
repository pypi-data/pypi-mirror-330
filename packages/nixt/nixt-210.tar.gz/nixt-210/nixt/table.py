# This file is placed in the Public Domain.


"table"


import importlib
import os
import threading
import types


from .errors import later
from .find   import spl
from .thread import launch


initlock = threading.RLock()
loadlock = threading.RLock()


class Table:

    debug  = False
    ignore = ["command", "names", "llm", "rst", "web", "udp", "wsd"]
    mods   = {}

    @staticmethod
    def add(mod) -> None:
        print(f"add {mod}")
        Table.mods[mod.__name__] = mod

    @staticmethod
    def all(pkg, mods="") -> [types.ModuleType]:
        path = pkg.__path__[0]
        pname = pkg.__name__
        res = []
        for nme in Table.modules(path):
            if nme in Table.ignore:
                continue
            if "__" in nme:
                continue
            if mods and nme not in spl(mods):
                continue
            name = pname + "." + nme
            if not name:
                continue
            mod = Table.load(name)
            if not mod:
                continue
            res.append(mod)
        return res

    @staticmethod
    def get(name) -> types.ModuleType:
        return Table.mods.get(name, None)

    @staticmethod
    def inits(names, pname) -> [types.ModuleType]:
        with initlock:
            mods = []
            for name in spl(names):
                mname = pname + "." + name
                if not mname:
                    continue
                mod = Table.load(mname)
                if not mod:
                    continue
                if "init" in dir(mod):
                    thr = launch(mod.init)
                mods.append((mod, thr))
            return mods

    @staticmethod
    def load(name) -> types.ModuleType:
        with loadlock:
            for ign in Table.ignore:
                if ign in name:
                    return
            pname = ".".join(name.split(".")[:-1])
            module = Table.mods.get(name)
            if not module:
                try:
                    Table.mods[name] = module = importlib.import_module(name, pname)
                    if Table.debug:
                        Table.mods[name].DEBUG = True
                except Exception as exc:
                    later(exc)
            return module

    @staticmethod
    def modules(path) -> [str]:
        return [
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and not x.startswith("__") and
                x not in Table.disable
               ]


def __dir__():
    return (
        'Table',
    )
