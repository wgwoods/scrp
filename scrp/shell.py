'''
scrp.shell - shell parser/simulator
'''

import os.path
from bashlex import parser, ast

from error import ShellError

class CmdResult(object):
    def __init__(self, retval, stdout='', stderr=''):
        self.retval = retval
        self.stdout = stdout
        self.stderr = stderr
    def __str__(self):
        return "CmdResult(retval={}, stdout={!r}, stderr={!r})".format(self.retval, self.stdout, self.stderr)

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

    def setenv(self, name, val):
        self.env[name] = val

    def add_command(self, path, handler):
        if callable(handler) or isinstance(handler, CmdResult):
            self.commands[path] = handler
        else:
            raise ValueError("command handler should be a CmdResult or a callable that returns one")

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

    def mock_run_command(self, node):
        print("  cmd: {}".format(node.cmd))
        ncmd = self._find_cmd(node.cmd[0])
        print("    binary: {}".format(ncmd))
        result = self.commands.get(ncmd, CmdResult(127))
        if callable(result):
            result = result(node.cmd)
        self.lastval = result.retval
        print("    result: {}".format(result))
        return result

    def visitcommand(self, node, parts):
        node.cmd = [n.word for n in parts if n.kind == 'word']
        node.result = self.mock_run_command(node)

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

class Command(object):
    '''Represents a mock command'''
    def __init__(self, path):
        self.path = path

class Groupadd(Command):
    pass
    # so this should have like:
    # declare your parser (as a dict of dicts)
    # a parse(argv) function that returns (opts)
    # a run(self, opts) function that takes `opts` and returns CmdResult
