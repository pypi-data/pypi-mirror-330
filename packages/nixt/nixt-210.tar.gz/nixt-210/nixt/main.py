# This file is placed in the Public Domain.


"main program"


import os
import pathlib
import signal
import sys
import time
import types
import _thread


from .cmnd    import Commands, Config, command, parse
from .errors  import Errors, later
from .find    import Workdir, pidname, spl
from .handler import Client, Event
from .object  import dumps
from .table   import Table
from .thread  import launch


p = os.path.join


def output(txt):
    print(txt)


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        output(txt.encode('utf-8', 'replace').decode("utf-8"))


class Console(CLI):

    def announce(self, txt):
        pass

    def callback(self, evt):
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt


"output"


def nil(txt):
    pass


def enable():
    global output
    output = print


def disable():
    global output
    output = nil


"utilities"


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    output(f"{Config.name.upper()} since {tme}")


def check(txt):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for c in txt:
            if c in arg:
                return True
    return False


def daemon(verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    os.nice(10)


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def inits(pkg, names) -> [types.ModuleType]:
    mods = []
    for name in modules(pkg.__path__[0]):
        if names and name not in spl(names):
            continue
        mname = pkg.__name__ + "." + name
        if not mname:
            continue
        mod = getattr(pkg, name, None)
        if not mod:
             continue
        if "init" in dir(mod):
           thr = launch(mod.init)
           mods.append((mod, thr))
    return mods


def modules(path) -> [str]:
    return [
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ]


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def scan(pkg, mods=""):
    res = []
    path = pkg.__path__[0]
    for nme in modules(path):
        if "__" in nme:
            continue
        if mods and nme not in spl(mods):
            continue
        name = pkg.__name__ + "." + nme
        if not name:
            continue
        mod = Table.load(name)
        if not mod:
            continue
        Commands.scan(mod)
        res.append(mod)
    return res


"handlers"


def handler(signum, frame):
     sys.exit(0)


"scripts"


def background():
    signal.signal(signal.SIGHUP, handler)
    daemon("-v" in sys.argv)
    Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")
    privileges()
    disable()
    pidfile(pidname(Config.name))
    Commands.add(cmd)
    Table,inits(Config.init or "irc,rss", Config.pname)
    forever()


def console():
    import readline # noqa: F401
    Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")
    enable()
    Commands.add(cmd)
    parse(Config, " ".join(sys.argv[1:]))
    Config.init = Config.sets.init or Config.init
    if "v" in Config.opts:
        banner()
    for _mod, thr in Table.inits(Config.init, Config.pname):
        if "w" in Config.opts:
            thr.join()
    csl = Console()
    csl.start()
    forever()


def control():
    if len(sys.argv) == 1:
        return
    Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")
    enable()
    Commands.add(cmd)
    Commands.add(srv)
    Commands.add(tbl)
    parse(Config, " ".join(sys.argv[1:]))
    csl = CLI()
    evt = Event()
    evt.orig = repr(csl)
    evt.type = "command"
    evt.txt = Config.otxt
    command(evt)
    evt.wait()


def service():
    Workdir.wdr = os.path.expanduser(f"~/.{Config.name}")
    enable()
    privileges()
    pidfile(pidname(Config.name))
    Commands.add(cmd)
    Table.inits(Config.init or "irc,rss", Config.pname)
    forever()


"commands"


def cmd(event):
    event.reply(",".join(sorted(Commands.names)))


def srv(event):
    import getpass
    name = getpass.getuser()
    event.reply(TXT % (Config.name.upper(), name, name, name, Config.name))


def tbl(event):
    from . import modules as MODS
    scan(MODS)
    event.reply("# This file is placed in the Public Domain.")
    event.reply("")
    event.reply("")
    event.reply('"lookup tables"')
    event.reply("")
    event.reply("")
    event.reply(f"NAMES = {dumps(Commands.names, indent=4, sort_keys=True)}")


"data"


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


"runtime"


def wrap(func):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        output("")
    except Exception as exc:
        later(exc)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    if check("c"):
        wrap(console)
    elif check("d"):
        signal.signal(signal.SIGHUP, handler)
        background()
    elif check("s"):
        wrap(service)
    else:
        control()


if __name__ == "__main__":
    main()
    for line in Errors.errors:
        output(line)
    sys.exit(0)
