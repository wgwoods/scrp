'''
scrp.cmdset.usergroup - cmdset for handling users/groups
'''

from shell import Command, CmdResult

#from collections import namedtuple
#Group = namedtuple("Group", "name pw id users")
#User = namedtuple("User", "name pw uid gid gecos homedir shell")

class UserGroup(object):
    def __init__(self):
        self.users = {}
        self.groups = {}

    def getent_cmd(self, argv):
        if len(argv) < 3:
            return CmdResult(1, 'getent: wrong number of arguments')
        db, key = argv[1:3]
        if db == "passwd":
            if key in self.users:
                return CmdResult(0, self.users[key])
            else:
                return CmdResult(1)
        elif db == "group":
            if key in self.groups:
                return CmdResult(0, self.groups[key])
            else:
                return CmdResult(1)
        else:
            return CmdResult(1, '', "Unknown database: {}".format(db))

    def useradd_cmd(self, argv):
        opts = self.useradd_parse(argv)

class Groupadd(Command):
    pass
    # TODO
    # so this should have like:
    # declare your parser (as a dict of dicts)
    # a parse(argv) function that returns (opts)
    # a run(self, opts) function that takes `opts` and returns CmdResult
