# -*- coding: utf-8 -*-
#
# vim: set ts=4 sw=4 sts=4 et :

import salt.config
import salt.grains.core
import subprocess
import re

__opts__ = salt.config.minion_config('/etc/salt/minion')
salt.grains.core.__opts__ = __opts__


def pci_devs():
    '''
    Useful PCI devices lists.
    '''
    def find_devices_of_class(klass):
        p = subprocess.Popen(["/sbin/lspci", "-mm", "-n"], stdout=subprocess.PIPE)
        result = p.communicate()
        retcode = p.returncode
        if retcode != 0:
            print "ERROR when executing lspci!"
            raise IOError

        rx_netdev = re.compile(r"^([0-9a-f]{2}:[0-9a-f]{2}.[0-9a-f]) \"" +
                               klass)
        for dev in str(result[0]).splitlines():
            match = rx_netdev.match(dev)
            if match is not None:
                dev_bdf = match.group(1)
                assert dev_bdf is not None
                yield dev_bdf

    grains = {
        'pci_net_devs': list(find_devices_of_class("02")),
        'pci_usb_devs': list(find_devices_of_class("0c03")),
    }

    return grains
