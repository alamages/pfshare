#!/usr/bin/env python3
#
# Copyright 2015: Emmanouil Kiagias <e.kiagias@gmail.com>
# License: GPLv3
#
import os
import sys
import atexit
import logging
import argparse
import socket
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
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

# this has the problem that is won't work if you don't
# have internet access
def get_local_ip():
    msocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        msocket.connect(('foss.aueb.gr', 80))
    except Exception:
        logging.exception('Error occured while resolving local ip.')
        sys.exit(1)
    else:
        local_ip = msocket.getsockname()[0]
        msocket.close()
        return local_ip

def get_port(port):
    # if port is not provided choose a random
    if not port:
        port = random.randint(7000, 8000)
    return port

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', dest='input_dir', type=str, default='.',
                        help='Directory to serve. Default is the current dir.')
    parser.add_argument('-p', '--port', dest='port', type=int, default=None,
                        help='Port which the http server will listen. \
                        If not provided a random is choosed')
    parser.add_argument('-q', '--quiet', dest='be_quiet', default=False,
                        action='store_true', help='Be quiet.')
    parser.add_argument('-l', '--local', dest='local', default=False,
                        action='store_true', help='Do not do port mapping in \
                        case the client is not behind NAT or client wants to\
                        share in LAN.')
    return parser.parse_args()

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

    return external_ip

def main():
    args = parse_args()

    if args.be_quiet:
        logging.basicConfig(format='logme: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='logme: %(message)s')

    if not os.path.isdir(args.input_dir):
        logging.error('%s is not a valid directory!' % args.input_dir)
        sys.exit(1)
    else:
        # cd to the path which will be served
        os.chdir(args.input_dir)

    port = get_port(args.port)
    external_ip = None

    # usually the client will be behind NAT
    if not args.local:
        external_ip = port_mapping(port)
    else:
        external_ip = get_local_ip()

    #logging.info('External ip: %s' % external_ip)

    # start the HTTP server:
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(('', port), handler)

    logging.error('Server is up at: http://%s:%d/' % (external_ip, port))
    httpd.serve_forever()

if __name__ == '__main__':
    main()
