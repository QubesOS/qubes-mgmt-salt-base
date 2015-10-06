# -*- coding: utf-8 -*-
# vim: set syntax=yaml ts=2 sw=2 sts=2 et :

##
# qubes.directories
# =================
#
# Set salt directory permissions
#
# TODO: Add option to pillar to specify dir permissions of all file_roots
#
# Execute:
#   qubesctl state.sls qubes.directories
##

# Qubes pillar file and directory permissions
# Note: using custom ID due to possible conflicts
directory_srv_pillar:
  file.directory:
    - name: /srv/pillar
    - user: root
    - group: root
    - dir_mode: 750
    - file_mode: 640
    - recurse:
      - user
      - group
      - mode

# Salt file and directory permissions
# Note: using custom ID due to possible conflicts
directory_srv_salt:
  file.directory:
    - name: /srv/salt
    - user: root
    - group: root
    - dir_mode: 750
    - file_mode: 640
    - recurse:
      - user
      - group
      - mode

# Qubes reactor file and directory permissions
# Note: using custom ID due to possible conflicts
directory_srv_reactor:
  file.directory:
    - name: /srv/reactor
    - user: root
    - group: root
    - dir_mode: 750
    - file_mode: 640
    - recurse:
      - user
      - group
      - mode

# salt-servers file and directory permissions
# Note: using custom ID due to possible conflicts
directory_srv_formulas:
  file.directory:
    - name: /srv/formulas
    - user: root
    - group: root
    - dir_mode: 750
    - file_mode: 640
    - recurse:
      - user
      - group
      - mode
