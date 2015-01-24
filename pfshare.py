#!/usr/bin/env python3
#
# Copyright 2015: Emmanouil Kiagias <e.kiagias@gmail.com>
# License: GPLv3
#
import sys
import atexit
import logger
import random
from miniupnpc import UPnP

logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)

upnpc = None
upnp_conf = {
	'external_port' : '',
	'protocol' : 'TCP', 
}

def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('-p', '--port', dest='port', type=int,
	                    help='Port which the http server will listen. \
	                    If not provided a random is choosed')
	parser.add_argument('-v', '--verbose', dest='be_verbose', default=False
						action='store_true', help='Be verbose.')
	parser.add_argument('-n', '--no-nat', dest='no_nat', default=False 
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

	upnpc = UPnP()
	upnpc.discover()

    #igd = upnpc.selectigd()
    #external_ip = upnpc.externalipaddress()
    #connection_type = upnpc.connectiontype()
    #local_ip = upnpc.lanaddr
    #AddPortMapping(externalPort, protocol, internalHost, internalPort, desc,
    #              remoteHost)
    #status = upnpc.addportmapping(8000, 'TCP', local_ip, 8000, "", "")
    #logger.info(status)

def main():
	args, extras = parse_args()

	if len(extras) != 0:
		logger.error('A single file or directory is allowed!')
		sys.exit(1)
	if args.be_verbose:
		logging.basicConfig(level=logging.INFO)

	port = get_port(args.port)
	external_ip = None

	# usually the client will be behind NAT
	if not no_nat:
		port_mapping(args.port)

	# TODO
if __name__ == "__main__":
    main()
