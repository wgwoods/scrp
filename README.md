# SCRP (**SCR**iptlet **P**arser)

This is a hacky set of tools to try to parse RPM scriptlets and convert
common parts of them to other forms of data.

## Try it out

It's barely functional at the moment but you can test it out like so:

```
    python scrp/cli.py < tests/scriptlets/radvd.prein.sh
```

Try feeding it other RPM scriptlets and watch it explode! Ha ha ha whee!

## TODO

* Finish support for the `usergroup` commands: `useradd`, `groupadd`, etc.
* Output `sysusers.d` snippets for user manipulation commands
* Handle file/symlink creation commands
* Output `tmpfiles.d` snippets for file/symlink creation commands
* ETC.
