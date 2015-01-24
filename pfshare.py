#!/usr/bin/env python3
#
# Copyright 2015: Emmanouil Kiagias <e.kiagias@gmail.com>
# License: GPLv3
#
import sys
import atexit
import logger
from miniupnpc import UPnP


def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('-p', '--port', dest='port', type=int,
	                    help='Port which the http server will listen. \
	                    If not provided a random is choosed')
	parser.add_argument('-v', '--verbose', dest='be_verbose', default=False
						action='store_true', help='Be verbose.')
	parser.add_argument('-n', '--no-nat', dest='no_nat', default=False 
						action='store_true', help='Do not do port mapping in \
						in case the client is not behind NAT.')
	return parser.parse_known_args()

def main():
    pass


if __name__ == "__main__":
    main()
