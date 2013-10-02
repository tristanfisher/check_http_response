check_http_response
===================

A python module to check an HTTP response either via JSON or plaintext.  Useful for nagios.


	usage: check_http_response.py [-h] [-v] [--server SERVER]
                              [--json JSON JSON | --text TEXT]

	A Nagios-ready python script for comparing data retrieved from an HTTP source.
	./check_http_response.py --host 'https://example.org/status' --json 'status'
	'ok'

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --version         Show script version and exit
	  --server SERVER, --host SERVER
                        specify a target host
	  --json JSON JSON      compares against a JSON key/value pair from a URI
	  --text TEXT           compares against a plain text response from a URI

###Requirements
+ [Python](http://www.python.org/)
+ The Python ['Requests' module](http://docs.python-requests.org/en/latest/user/install/#install)

###Documentation
The documentation is available via the '-h' or '--help' flag to the check_http_response command.  If you would like additional documentation, please request via opening an 'issue' on this repo.

###Contribute

1. Fork the repository on GitHub to start making your changes to the **master** branch (or branch off of it).
2. Write a test which shows that the bug was fixed or that the feature works as expected.
3. Send a pull request and bug the maintainer until it gets merged and published.
