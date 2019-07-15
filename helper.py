#!/usr/bin/env python3

import argparse
import os, binascii
import textwrap

def random_hex(length):
    return binascii.b2a_hex(os.urandom(length))

def parse_arguments():
    """argument parser"""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'iface',
        type=int,
        help='uci wifi iface index\n'
             'you can obtain the uci index by looking for your ssid:\n'
             '  uci get wireless.@wifi-iface[0].ssid\n'
             '  uci get wireless.@wifi-iface[1].ssid\n'
             '  ...')
    parser.add_argument(
        '--ap',
        action='append',
        help=('bssid(s) of access point(s)'))
    parser.add_argument(
        '--format',
        choices=['uci','config'],
        default='uci',
        help='output format\n'
             '  uci: prints uci commands (default)\n'
             '  config: prints config file snippets')
    return parser.parse_args()

if __name__ == '__main__':
    ARGS = parse_arguments()
    password = random_hex(16).decode()
    mobility_domain = random_hex(2).decode()
    if 'uci' in ARGS.format:
        output_prefix = 'uci set wireless.@wifi-iface[{}].'.format(ARGS.iface)
        output_seperator = '='
    elif 'config' in ARGS.format:
        output_prefix = '\toption '
        output_seperator = ' '
    r0kh = []
    r1kh = []
    for bssid in ARGS.ap:
        nasid = bssid.replace(':', '')
        r0kh.append('{},{},{}'.format(bssid, nasid, password))
        r1kh.append('{},{},{}'.format(bssid, bssid, password))

    for bssid in ARGS.ap:
        nasid = bssid.replace(':', '')
        print('---Madkodur rooming --------------------------------\n')
        print('Configuration for AP with BSSID {}:\n'.format(bssid))
        print('{}ieee80211r{}\'1\''.format(output_prefix, output_seperator))
        print('{}mobility_domain{}\'{}\''.format(output_prefix, output_seperator, mobility_domain))
        print('{}pmk_r1_push{}\'1\''.format(output_prefix, output_seperator))
        print('{}nasid{}\'{}\''.format(output_prefix, output_seperator, nasid))
        print('{}r1_key_holder{}\'{}\''.format(output_prefix, output_seperator, nasid))
        if 'uci' in ARGS.format:
            print('{}r0kh=\'{}\''.format(output_prefix, ' '.join(r0kh)))
            print('{}r1kh=\'{}\''.format(output_prefix, ' '.join(r1kh)))
        elif 'config' in ARGS.format:
            for r0kh_item in r0kh:
                print('\tlist r0kh \'{}\''.format(r0kh_item))
            for r1kh_item in r1kh:
                print('\tlist r1kh \'{}\''.format(r1kh_item))
    if 'uci' in ARGS.format:
        print('\nDo not forget to save your changes with \'uci commit wireless\'')
    print('\nApply your settings with \'wifi restart\'\n')
