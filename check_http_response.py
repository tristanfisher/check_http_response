#!/usr/bin/env python

import json
import requests
import sys
import subprocess
import argparse

VERSION='1.06'
def show_version(): print(VERSION)

class Nagios:
    ok          = (0, 'OK')
    warning     = (1, 'WARNING')
    critical    = (2, 'CRITICAL')
    unknown     = (3, 'UNKNOWN')

nagios = Nagios()

def nagiosExit(exit_code,msg=None):
    """Exit script with a str() message and an integer 'nagios_code', which is a sys.exit level."""
    if msg:
        print(exit_code[0],exit_code[1] + " - " + str(msg))
    sys.exit(exit_code[0])

def uri_request(uri, expected_response_format=None, arg0=None, arg1=None, headers_only=False):
    try:
        if headers_only == True:  request = requests.head(uri)
        else: request = requests.get(uri)

        if request.status_code > 200:
            nagiosExit(nagios.critical, str("Status code: {0} :: {1}".format(request.status_code, uri)))
        else:
            if expected_response_format == 'JSON':
                try:
                    json_response = json.loads(request.text)
                except ValueError:
                    nagiosExit(nagios.critical, str("Could not decode valid JSON at URI: {0}".format(uri)))
                check_json_response(json_response, check_json_key=arg0, check_json_value=arg1)
            else:
                text_response = str(request.content) #be careful on strings that could look like other types
                check_text_response(text_response, arg0)

    except requests.ConnectionError : nagiosExit(nagios.critical,str("Error loading :: {0}".format(uri)))
    except requests.Timeout : nagiosExit(nagios.critical,str("Timed out :: {0}".format(uri)))
    except requests.HTTPError : nagiosExit(nagios.critical,str("Invalid HTTP response :: {0}".format(uri)))
    except requests.TooManyRedirects: nagiosExit(nagios.critical,str("Too many redirects :: {0}".format(uri)))

def check_json_response(json_response,check_json_key,check_json_value):
    """ check a json key/value pair against a HTTP response.
    match returns nagiosExit(0), otherwise nagiosExit(1) is returned.
    """
    try:
        if json_response[check_json_key] != check_json_value:
            returnValue = "Expected '{0}:{1}' ; Received '{2}'".format(check_json_key, check_json_value, json_response[check_json_key])
            nagiosExit(nagios.critical, str(returnValue))
        else:
            nagiosExit(nagios.ok)
    except KeyError:
        ''' key could not be looked up in the response data from the URI '''
        nagiosExit(nagios.critical, str("KeyError :: Failed to find JSON key: {0}").format(check_json_value))


def check_text_response(text_response,expected_response_text):
    """ Simply do an equality comparison between two objects.  Caution, may do 'hilarious' things on binary data. """
    if str(text_response) != str(expected_response_text):
        returnValue = "Expected {0} ; Received: {1}".format(expected_response_text, text_response)
        nagiosExit(nagios.critical,str(returnValue))
    else:
        nagiosExit(nagios.ok)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=str("A Nagios-ready python script for comparing data retrieved from an HTTP source.\n ./check_http_response.py --host 'https://example.org/status' --json 'status' 'ok'"))
    parser.add_argument('-v', '--version', action="store_true", help='Show script version and exit')
    parser.add_argument('--server', '--host', help="specify a target host", type=str)
    parser.add_argument('--headers_only', help="retrieve only the headers", action='store_true', default=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--json', nargs=2, help="compares against a JSON key/value pair from a URI", type=str)
    group.add_argument('--text', nargs=1, help="compares against a plain text response from a URI")

    args = parser.parse_args()

    if args.version:
        show_version()
    if args.json:
        uri_request(uri=args.server, expected_response_format='JSON', arg0=args.json[0], arg1=args.json[1],
                headers_only=args.headers_only)
    if args.text:
        uri_request(uri=args.server, expected_response_format='text', arg0=str(args.text[0]),
                headers_only=args.headers_only)
    if not args.version or args.json or args.text:
        parser.print_help()
        sys.exit(0)
