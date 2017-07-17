getent group radvd >/dev/null || groupadd -r -g 75 radvd
getent passwd radvd >/dev/null || \
  useradd -r -u 75 -g radvd -d / -s /sbin/nologin -c "radvd user" radvd
exit 0