Info
-----

`pfshare.py` script starts an HTTP server which serves files from a given directory and below.  The script uses `miniupnpc` (for port forwarding) so the client's files can be easily  served behind NAT.

Dependencies
------------

* python3 
* [miniupnpc](https://github.com/miniupnp/miniupnp/tree/master/miniupnpc) (installpythonmodule3)

Usage
--------
For available arguments run the script with `-h` argument (or `--help)`  
Some usage examples:

`$ # serves the current directory behind NAT in a random port`  
`$./pfshare.py`

`$ # serves my_dir in port 8000`  
`$ ./pfshare -d my_dir -p 8000`

`$ # serves but only locally (no port forwarding is performed)`  
`$ ./pfshare.py -l`

TODO
-----

* add more fancy stuff into the script