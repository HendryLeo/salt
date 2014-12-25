# -*- coding: utf-8 -*-
'''
Display salt-key output
=======================

The ``salt-key`` command makes use of this outputter to format its output.
'''
from __future__ import absolute_import

# Import salt libs
import salt.utils
import salt.output


def output(data):
    '''
    Read in the dict structure generated by the salt key API methods and
    print the structure.
    '''
    color = salt.utils.get_colors(__opts__.get('color'))
    strip_colors = __opts__.get('strip_colors', True)
    if __opts__['transport'] == 'zeromq':
        acc = 'minions'
        pend = 'minions_pre'
        den = 'minions_denied'
        rej = 'minions_rejected'

        cmap = {pend: color['RED'],
                acc: color['GREEN'],
                den: color['MAGENTA'],
                rej: color['BLUE'],
                'local': color['MAGENTA']}

        trans = {pend: u'{0}Unaccepted Keys:{1}'.format(
                                    color['LIGHT_RED'],
                                    color['ENDC']),
                 acc: u'{0}Accepted Keys:{1}'.format(
                                    color['LIGHT_GREEN'],
                                    color['ENDC']),
                 den: u'{0}Denied Keys:{1}'.format(
                                    color['LIGHT_MAGENTA'],
                                    color['ENDC']),
                 rej: u'{0}Rejected Keys:{1}'.format(
                                    color['LIGHT_BLUE'],
                                    color['ENDC']),
                 'local': u'{0}Local Keys:{1}'.format(
                                    color['LIGHT_MAGENTA'],
                                    color['ENDC'])}
    else:
        acc = 'accepted'
        pend = 'pending'
        rej = 'rejected'

        cmap = {pend: color['RED'],
                acc: color['GREEN'],
                rej: color['BLUE'],
                'local': color['MAGENTA']}

        trans = {pend: u'{0}Unaccepted Keys:{1}'.format(
                                    color['LIGHT_RED'],
                                    color['ENDC']),
                 acc: u'{0}Accepted Keys:{1}'.format(
                                    color['LIGHT_GREEN'],
                                    color['ENDC']),
                 rej: u'{0}Rejected Keys:{1}'.format(
                                    color['LIGHT_BLUE'],
                                    color['ENDC']),
                 'local': u'{0}Local Keys:{1}'.format(
                                    color['LIGHT_MAGENTA'],
                                    color['ENDC'])}

    ret = ''

    for status in sorted(data):
        ret += u'{0}\n'.format(trans[status])
        for key in data[status]:
            skey = key
            if strip_colors:
                skey = salt.output.strip_esc_sequence(key)
            if isinstance(data[status], list):
                ret += u'{0}{1}{2}\n'.format(
                        cmap[status],
                        skey,
                        color['ENDC'])
            if isinstance(data[status], dict):
                ret += u'{0}{1}:  {2}{3}\n'.format(
                        cmap[status],
                        skey,
                        data[status][key],
                        color['ENDC'])
    return ret
