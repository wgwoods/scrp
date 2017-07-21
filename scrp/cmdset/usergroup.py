'''
scrp.cmdset.usergroup - cmds for handling users/groups
'''

from shell import Command, CmdResult

#from collections import namedtuple
#Group = namedtuple("Group", "name pw id users")
#User = namedtuple("User", "name pw uid gid gecos homedir shell")

class Getent(Command):
    def init(self):
        self.shell.ctx.users = {}
        self.shell.ctx.groups = {}
        self.parser.add_argument("db")
        self.parser.add_argument("key")

    def run(self, opts, args):
        if opts.db == "passwd":
            if opts.key in self.shell.ctx.users:
                return CmdResult(0, self.shell.ctx.users[key])
            else:
                return CmdResult(1)
        elif opts.db == "group":
            if opts.key in self.shell.ctx.groups:
                return CmdResult(0, self.shell.ctx.groups[key])
            else:
                return CmdResult(1)
        else:
            return CmdResult(1, '', "Unknown database: {}".format(opts.db))

class Useradd(Command):
    def init(self):
        self.shell.ctx.users = {}
        self.shell.ctx.groups = {}
        p = self.parser
        p.add_argument("--skel", "-k")
        p.add_argument("--gid", "-g")
        p.add_argument("--groups", "-G", type=lambda a: a.strip().split(','))
        p.add_argument("--shell", "-s")
        p.add_argument("--uid", "-u")
        p.add_argument("--home-dir", "-d")
        p.add_argument("--comment", "-c")
        p.add_argument("--base-dir", "-b", default="/home")
        p.add_argument("--non-unique", "-o", action='store_true')
        p.add_argument("--system", "-r", action='store_true')
        p.add_argument("--no-log-init", "-l", action='store_true')
        p.add_argument("--create-home", "-m", action='store_true')
        p.add_argument("-M", dest='create_home', action='store_false')
        p.add_argument("--user-group", "-U", action='store_true')
        p.add_argument("--no-user-group", "-N", dest='user_group', action='store_false')
        p.add_argument("name")

    def run(self, opts, args):
        self.shell.ctx.users[opts.name] = opts
        return CmdResult(0)

class Groupadd(Command):
    def init(self):
        self.parser.add_argument("--gid", "-g")
        self.parser.add_argument("--system", "-r", action='store_true')
        self.parser.add_argument("--force", "-f", action='store_true')
        self.parser.add_argument("--non-unique", "-o", action='store_true')
        self.parser.add_argument("name")
        self.shell.ctx.groups = {}

    def run(self, opts, args):
        self.shell.ctx.groups[opts.name] = opts
        return CmdResult(0)
