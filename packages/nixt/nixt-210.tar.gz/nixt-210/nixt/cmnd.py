# This file is placed in the Public Domain.


"commands"


import inspect
import time
import typing


from .errors import later
from .object import Default
from .table  import Table


STARTTIME = time.time()


class Config(Default):

    init = ""
    name = Default.__module__.split(".")[0]
    pname = f"{name}.modules"
    opts = Default()


try:
    from .names import NAMES
except Exception as ex:
    later(ex)
    NAMES = {}


class Commands:

    cmds = {}
    names = NAMES

    @staticmethod
    def add(func, mod=None) -> None:
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__

    @staticmethod
    def get(cmd) -> typing.Callable:
        func = Commands.cmds.get(cmd, None)
        if not func:
            name = Commands.names.get(cmd)
            if name:
                mod = Table.load(name)
                Commands.scan(mod)
                func = Commands.cmds.get(cmd)
        return func

    @staticmethod
    def getname(cmd) -> None:
        return Commands.names.get(cmd)

    @staticmethod
    def scan(mod) -> None:
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz, mod)


def command(evt) -> None:
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.display()
    evt.ready()


def parse(obj, txt=None) -> None:
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Default()
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = {}
    obj.sets    = Default()
    obj.txt     = txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def __dir__():
    return (
        'STARTTIME',
        'Commands',
        'command',
        'parse'
    )
