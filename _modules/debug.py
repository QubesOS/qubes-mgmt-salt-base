# -*- coding: utf-8 -*-
#
# vim: set ts=4 sw=4 sts=4 et :
'''
:maintainer:    Jason Mehring <nrgaway@gmail.com>
:maturity:      new
:platform:      all

===========================
Qubes test modules for salt
===========================
'''

# Import python libs
import argparse
import logging

from inspect import getargvalues, stack

# Salt + Qubes libs
import module_utils

from qubes_utils import function_alias as _function_alias
from module_utils import ModuleBase as _ModuleBase

# Enable logging
log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = 'debug'


def __virtual__():
    '''
    '''
    return __virtualname__

#__outputter__ = {
#    'get_prefs': 'txt',
#}


class _TestBase(_ModuleBase):
    '''Overrides.
    '''
    def __init__(self, *varargs, **kwargs):
        '''
        '''
        if not hasattr(module_utils, '__opts__'):
            module_utils.__opts__ = __opts__
        if not hasattr(module_utils, '__salt__'):
            module_utils.__salt__ = __salt__

        super(_TestBase, self).__init__(*varargs, **kwargs)


def mode(*varargs, **kwargs):
    '''
    Sets debug mode for all or specific states status:

    Pass module names to enable or disable.

    Valid actions:

    .. code-block:: yaml

        # Optional
        - enable-all:           [True]
        - disable-all:          [True]
        - enable:               [MODULE ...]
        - disable:              [MODULE ...]
    '''
    #self.arg_options_create(argv_ordering=['flags', 'args', 'varargs', 'keywords'])
    base = _TestBase('debug.mode', **kwargs)
    base.parser.add_argument('--status-mode', nargs='*', default=['all'], choices=('last', 'all', 'debug', 'debug-changes'), help=argparse.SUPPRESS)
    base.parser.add_argument('id', nargs='?', help=argparse.SUPPRESS)
    base.parser.add_argument('--enable-all', nargs='?', type=bool, default=False, help='Enable debug mode for all modules')
    base.parser.add_argument('--disable-all', nargs='?', type=bool, default=False, help='Disable debug mode for all modules')
    base.parser.add_argument('--enable', nargs='+', default=False, help='Enable debug mode for provided modules')
    base.parser.add_argument('--disable', nargs='+', default=False, help='Disable debug mode for provided modules')
    args = base.parse_args(*varargs, **kwargs)

    # Enable
    if args.enable_all:
        if '__all__' not in base._debug_mode:
            base._debug_mode.append('__all__')
            base.save_status(message='Enabled \'ALL\'')
        else:
            base.save_status(prefix='[SKIP] ', message='Already enabled \'ALL\'')
    elif args.enable:
        for module in args.enable:
            if module not in base._debug_mode:
                base._debug_mode.append(module)
                base.save_status(message='Enabled \'{0}\''.format(module))
            else:
                base.save_status(prefix='[SKIP] ', message='Already enabled \'{0}\''.format(module))

    # Disable
    if args.disable_all:
        for module in sorted(base._debug_mode, reverse=True):
            base._debug_mode.remove(module)
            base.save_status(message='Disabled \'{0}\''.format(module))
    elif args.disable:
        for module in args.disable:
            if module in base._debug_mode:
                base._debug_mode.remove(module)
                base.save_status(message='Disabled \'{0}\''.format(module))
            else:
                base.save_status(prefix='[SKIP] ', message='Already disabled \'{0}\''.format(module))

    # Returns the status 'data' dictionary
    return base.status()
