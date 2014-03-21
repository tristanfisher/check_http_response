check_http_response
===================

A python module to check an HTTP response either via JSON or plaintext.  Useful for nagios.

		usage: check_http_response.py [-h] [-v] [--server SERVER] [--headers_only]
									  [--json JSON JSON | --text TEXT]

		A Nagios-ready python script for comparing data retrieved from an HTTP source.
		./check_http_response.py --host 'https://example.org/status' --json 'status'
		'ok'

		optional arguments:
		  -h, --help            show this help message and exit
		  -v, --version         Show script version and exit
		  --server SERVER, --host SERVER
								specify a target host
		  --headers_only        retrieve only the headers
		  --json JSON JSON      compares against a JSON key/value pair from a URI
		  --text TEXT           compares against a plain text response from a URI


#####A word of caution with checking text:

If you plan on checking a text file, you likely want to write data to the file without a newline.

e.g. use the following:

`$ echo -n 'ok' > /var/www/testpage.html`

Otherwise, you're actually putting in the contents `'ok\n'` and *may be surprised* by the check returning an error.

e.g. you may run into the following:

`$ echo 'ok' > /var/www/testpage.html` *#echo adds a newline :(*

`$ ./check_http_response.py --server 'http://example.org/testpage.html' --text 'ok'`

`(2, "CRITICAL - Expected ok ; Received: ok\n]")`


This is not a flaw in check_http_response or tools such as echo.  The latter tries to be helpful (most of the time, you want a newline) and the prior by design should be strict in its comparisons.


###Requirements
+ [Python](http://www.python.org/)
+ The Python ['Requests' module](http://docs.python-requests.org/en/latest/user/install/#install)

###Documentation
The documentation is available via the '-h' or '--help' flag to the check_http_response command.  If you would like additional documentation, please request via opening an 'issue' on this repo.

###Contribute

1. Fork the repository on GitHub to start making your changes to the **master** branch (or branch off of it).
2. Write a test which shows that the bug was fixed or that the feature works as expected.
3. Send a pull request and bug the maintainer until it gets merged and published.
