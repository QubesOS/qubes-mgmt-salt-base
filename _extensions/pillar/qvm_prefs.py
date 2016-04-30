#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2016  Marek Marczykowski-Górecki
#                                   <marmarek@invisiblethingslab.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#

in_dom0 = True
try:
    from qubes.qubes import QubesVmCollection
except ImportError:
    in_dom0 = False


def __virtual__():
    return in_dom0


def ext_pillar(minion_id, pillar, *args, **kwargs):
    qc = QubesVmCollection()
    qc.lock_db_for_reading()
    qc.load()
    qc.unlock_db()
    vm = qc.get_vm_by_name(minion_id)
    if vm is None:
        return {}
    qvm_pillar = {}
    if vm.qid == 0:
        qvm_pillar['type'] = 'admin'
    elif vm.is_template():
        qvm_pillar['type'] = 'template'
    elif vm.template is None:
        qvm_pillar['type'] = 'standalone'
    else:
        qvm_pillar['type'] = 'app'

    if vm.template:
        qvm_pillar['template'] = vm.template.name

    if vm.netvm:
        qvm_pillar['netvm'] = vm.netvm.name

    # TODO: consider other properties; target VM will learn them!

    return {'qubes': qvm_pillar}
