#!/usr/bin/env python

import json,requests,sys

VERSION='0.01'
def show_version(): print(VERSION)

class Nagios:
    ok          = (0, 'OK')
    warning     = (1, 'WARNING')
    critical    = (2, 'CRITICAL')
    unknown     = (3, 'UNKNOWN')

nagios = Nagios()

def s(x):
    """return a string encoded equivalent of input.  paranoid check meant as a quick decorator."""
    return str(x)

def nagiosExit(exit_code,msg=None):
    """Exit script with a str() message and an integer 'nagios_code', which is a sys.exit level.

    Named nagiosExit to avoid confusion with sys.exit
    """
    if (msg == None):
        sys.exit(nagios.ok[0])
    else:
        print(exit_code[0],exit_code[1] + " - " + str(msg))
        sys.exit(exit_code[0])

#TODO: generalize a check_response function and only then call a function to compare the data
# def get_uri_response(uri); def_check_json() or def_check_content()

def check_text_response(uri, expected_response_data):
    """ Check URI for any (even binary data) content."""

    def checkMatch(data_response, expected_response_data):
        """ Simply do an equality comparison between two objects.  Caution, may do 'hilarious' things on binary data. """
        try:
            if data_response != expected_response_data:
                returnValue = "{0} :: expected {1} received {2}".format(data_response, expected_response_data)
                nagiosExit(nagios.critical, str(returnValue))
            else:
                nagiosExit(nagios.ok)
        except:
            nagiosExit(nagios.critical, str("{0} :: Failed to grab/parse data {1}").format(uri, data_response))
    try:
        request = requests.get(uri)
        if request.status_code > 200:
            nagiosExit(nagios.critical,str("Status code: {0} :: {1}".format(request.status_code, uri)))
        else:
            data_response = request.content
            checkMatch(data_response, expected_response_data)

    except requests.ConnectionError:
        nagiosExit(nagios.critical,str("Error loading :: {0}".format(uri)))
    except requests.Timeout:
        nagiosExit(nagios.critical,str("Timed out :: {0}".format(uri)))
    except requests.HTTPError:
        nagiosExit(nagios.critical,str("Invalid HTTP response :: {0}".format(uri)))
    except requests.TooManyRedirects:
        nagiosExit(nagios.critical,str("Too many redirects :: {0}".format(uri)))

    if request.text != expected_response_data:
        nagiosExit(nagios.critical,str("{0} :: "))
    else:
        nagiosExit(nagios.ok)

def check_json_response(uri, response_key, expected_response_key_data):
    """ check a json key/value pair against a HTTP URI.
    match returns nagiosExit(0), otherwise nagiosExit(1) is returned.
    """

    def checkMatch(json_response, response_key, expected_response_key_data):
        try:
            if json_response[response_key] != expected_response_key_data:
                returnValue = "{0} :: expected '{1}:{2}' received '{3}'".format(uri, response_key, expected_response_key_data, json_response[response_key])
                nagiosExit(nagios.critical, str(returnValue))
            else:
                nagiosExit(nagios.ok)
        except KeyError:
            nagiosExit(nagios.critical, str("{0} :: Failed to find JSON key: {1}").format(uri, response_key))

    try:
        request = requests.get(uri)
        if request.status_code > 200:
            nagiosExit(nagios.critical,str("Status code: {0} :: {1}".format(request.status_code, uri)))
        else:
            json_response = json.loads(request.text)
            checkMatch(json_response, response_key, expected_response_key_data)

    #consider using unknown, depending on context.  nagios.critical is a sane default because an unknown
    #status is often just as bad as an erroneous state..
    except requests.ConnectionError:
        nagiosExit(nagios.critical,str("Error loading :: {0}".format(uri)))
    except requests.Timeout:
        nagiosExit(nagios.critical,str("Timed out :: {0}".format(uri)))
    except requests.HTTPError:
        nagiosExit(nagios.critical,str("Invalid HTTP response :: {0}".format(uri)))
    except requests.TooManyRedirects:
        nagiosExit(nagios.critical,str("Too many redirects :: {0}".format(uri)))

import argparse
parser = argparse.ArgumentParser(description=str("A Nagios-ready python script for comparing data retrieved from an HTTP source.\n ./check_http_response.py --host 'https://example.org/status' --json 'status' 'ok'"))
parser.add_argument('-v', '--version', action="store_true", help='Show script version and exit')
parser.add_argument('--server', '--host', help="specify a target host", type=str)

group = parser.add_mutually_exclusive_group()
group.add_argument('--json', nargs=2, help="compares against a JSON key/value pair from a URI", type=str)
group.add_argument('--text', nargs=1, help="compares against a plain text response from a URI")

args = parser.parse_args()

if args.version:
    show_version()
if args.json:
    check_json_response(args.server, args.json[0], args.json[1])
if args.text:
    check_text_response(args.server, args.text)

#def test():
#    check_json_response('https://example.org/status', 'status', 'ok')

#if __name__ == "__main__":
#    test()

