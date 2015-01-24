#!/usr/bin/env python3
#
# Copyright 2015: Emmanouil Kiagias <e.kiagias@gmail.com>
# License: GPLv3
#
import sys
import atexit
import logging
import argparse
import random
from miniupnpc import UPnP

upnpc = None
upnp_conf = {
    'external_port' : '',
    'protocol' : 'TCP',
}

def clean_up():
    logging.info('Clean up function was called.')

    if upnpc:
        logging.info('Deleting port mapping...')
        upnpc.deleteportmapping(upnp_conf['external_port'],
                                upnp_conf['protocol'], '')
    else:
        logging.info('Nothing to clean up.')

atexit.register(clean_up)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', dest='port', type=int, default=None,
                        help='Port which the http server will listen. \
                        If not provided a random is choosed')
    parser.add_argument('-v', '--verbose', dest='be_verbose', default=False,
                        action='store_true', help='Be verbose.')
    parser.add_argument('-n', '--no-nat', dest='no_nat', default=False,
                        action='store_true', help='Do not do port mapping in \
                        in case the client is not behind NAT or client wants to\
                        share in LAN.')
    return parser.parse_known_args()

def get_port(port):
    # if port is not provided choose a random
    if not port:
        port = random.randint(7000, 8000)

    return port

def port_mapping(port):
    upnp_conf['external_port'] = port

    global upnpc
    upnpc = UPnP()
    upnpc.discover()
    upnpc.selectigd()

    external_ip = upnpc.externalipaddress()
    local_ip = upnpc.lanaddr
    # externalPort, protocol, internalHost, internalPort, desc,
    # remoteHost)
    logging.info('UPnP port mapping, port: %d' % port)
    success = upnpc.addportmapping(port, upnp_conf['protocol'],
                                   local_ip, port, 'pfshare upnp', '')
    if not success:
        logging.error('Error occured in port mapping function!')
        sys.exit(1)

def main():
    args, extras = parse_args()
    
    if len(extras) != 0:
        logging.error('A single file or directory is allowed!')
        sys.exit(1)
    if args.be_verbose:
        logging.basicConfig(level=logging.INFO, format='logme: %(message)s')
        logging.info('Verbose mode enabled.')
    else:
    	logging.basicConfig(format='logme: %(message)s')

    port = get_port(args.port)
    external_ip = None

    # usually the client will be behind NAT
    if not args.no_nat:
        port_mapping(port)


if __name__ == "__main__":
    main()
