'''
scrp.cmd - command entrypoints for CLI tools.
'''

from shell import MockShell
from cmdset.usergroup import UserGroup

# TOOD: this will get repetitive as we add more entrypoints.
# Could be using argparse with like `--cmdset=usergroup` to turn on
# individual usergroups as needed...
def main():
    import sys
    sh = MockShell()
    users = UserGroup()
    sh.add_command("/usr/bin/getent", users.getent_cmd)
    body = sys.stdin.read()
    sh.run(body)

if __name__ == '__main__':
    main()
