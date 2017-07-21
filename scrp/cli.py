'''
scrp.cmd - command entrypoints for CLI tools.
'''

from shell import MockShell
from cmdset.usergroup import Getent, Groupadd, Useradd

# TOOD: this will get repetitive as we add more entrypoints.
# Could be using argparse with like `--cmdset=usergroup` to turn on
# individual usergroups as needed...
def main():
    import sys
    sh = MockShell()
    sh.add_command("/usr/bin/getent", Getent)
    sh.add_command("/usr/bin/groupadd", Groupadd)
    sh.add_command("/usr/bin/useradd", Useradd)
    body = sys.stdin.read()
    sh.run(body)
    print("")
    print(sh.ctx)

if __name__ == '__main__':
    main()
