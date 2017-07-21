'''
scrp.shell - shell parser/simulator
'''

import os.path
from bashlex import parser, ast
from argparse import ArgumentParser, Namespace, ArgumentError

from error import ShellError

# TODO: should this be CommandResult for consistency?
class CmdResult(object):
    def __init__(self, retval, stdout='', stderr=''):
        self.retval = retval
        self.stdout = stdout
        self.stderr = stderr
    def __str__(self):
        return "CmdResult(retval={}, stdout={!r}, stderr={!r})".format(self.retval, self.stdout, self.stderr)

CommandNotFound = CmdResult(127) # TODO: stderr?

class Command(object):
    def __init__(self, shell):
        self.shell = shell
        self.parser = ArgumentParser()
        self.init()

    def init(self):
        pass

    def parse(self, argv):
        # FIXME: handle ArgumentError cleanly
        return self.parser.parse_known_args(argv)

    def run(self, opts, args):
        return CmdResult(0)

    def __call__(self, argv):
        opts, args = self.parse(argv)
        return self.run(opts, args)

class MockShell(ast.nodevisitor):
    default_env = {
        'PATH':'/usr/bin:/usr/sbin:/bin:/sbin',
    }

    default_commands = {
        '/bin/:': CmdResult(0),
        '/bin/true': CmdResult(0),
        '/bin/false': CmdResult(1),
        '/bin/exit': lambda argv: CmdResult(int(argv[1]))
    }

    def __init__(self):
        self.lastval = 0
        self.wd = '/'

        self.commands = {}
        for path, handler in self.default_commands.items():
            self.add_command(path, handler)

        self.env = {}
        for name, val in self.default_env.items():
            self.setenv(name, val)

        self.ctx = Namespace()

    def setenv(self, name, val):
        self.env[name] = val

    def add_command(self, path, handler):
        if type(handler) == type(Command) and issubclass(handler, Command):
            self.commands[path] = handler(self)
        elif isinstance (handler, CmdResult):
            self.commands[path] = lambda argv: handler
        elif callable(handler):
            self.commands[path] = handler
        else:
            raise ValueError("handler should be Command, CmdResult, or callable that returns CmdResult")

    def _find_cmd(self, cmd):
        if os.path.isabs(cmd):
            ncmd = os.path.normpath(cmd)
            if ncmd in self.commands:
                return ncmd
        elif '/' in cmd:
            return self._find_cmd(os.path.join(self.wd, cmd))
        else:
            for p in self.env.get('PATH').split(':'):
                ncmd = self._find_cmd(os.path.join(p, cmd))
                if ncmd:
                    return ncmd

    def _run_cmd(self, cmd, argv):
        handler = self.commands.get(cmd, CommandNotFound)
        if isinstance(handler, CmdResult):
            return handler
        elif callable(handler):
            return handler(argv)
        else:
            raise ValueError("bad handler for {}: {}".format(cmd, handler))

    # TODO: make debug output configurable
    def mock_run_command(self, argv):
        print("  argv: {}".format(argv))

        cmd = self._find_cmd(argv[0])
        print("    binary: {}".format(cmd))

        result = self._run_cmd(cmd, argv)
        print("    result: {}".format(result))

        self.lastval = result.retval
        return result

    def visitcommand(self, node, parts):
        # FIXME: Is this correct when there's redirects etc?
        node.argv = [n.word for n in parts if n.kind == 'word']
        node.result = self.mock_run_command(node.argv)

    def visitlist(self, node, parts):
        print("start cmd list")
        for n in parts:
            if n.kind == "command":
                self.visit(n)
            elif n.kind == "operator":
                if n.op == '&&':
                    if self.lastval == 0:
                        print("  &&: continue")
                    else:
                        print("  &&: break ($?={})".format(self.lastval))
                        break
                elif n.op == '||':
                    if self.lastval != 0:
                        print("  ||: continue")
                    else:
                        print("  ||: break ($?={})".format(self.lastval))
                        break
                else:
                   raise ShellError("Unhandled operator {!r}".format(n.op), node)
            else:
                raise ShellError("Unhandled node", node)
        print("end cmd list, result {}\n".format(self.lastval))
        return False

    def run(self, body, dump=False):
        # HACK: bashlex crashes on empty lines >_<
        import re
        body = re.sub(r'\n+', "\n", body)
        # parse it and walk through the tree
        for tree in parser.parse(body):
            if dump:
                print(tree.dump())
            self.visit(tree)
