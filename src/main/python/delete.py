#!/usr/bin/python

import urllib2
import ssl
import json
import traceback
import sys


# Delete all dashboards in an Org

def list_dashboards(url, key):
    req = urllib2.Request("%s/api/search" % url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    try:
        context = ssl.SSLContext(
            ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
        result = urllib2.urlopen(req, context=context)
        if result:
            return result

    except urllib2.HTTPError as e:
        traceback.print_exc()


def delete_dashboard(url, key, id):
    req = urllib2.Request(
        "%s/api/dashboards/uid/%s" % (url, id))
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    req.get_method = lambda: 'DELETE'

    try:
        context = ssl.SSLContext(
            ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
        result = urllib2.urlopen(req, context=context)
        if result:
            return result

    except urllib2.HTTPError as e:
        traceback.print_exc()


if len(sys.argv) < 3:
    print 'Usage: delete.py <grafanaURL> <apiKey>'
    sys.exit(1)

url = sys.argv[1]
key = sys.argv[2]

dashboards = json.load(list_dashboards(url, key))

print dashboards
for dashboard in dashboards:
    if dashboard['type'] == 'dash-db':  # don't delete folders only dashboards
        print 'Deleting %s %s' % (dashboard['title'], dashboard['uid'])
        delete_dashboard(url, key, dashboard['uid'])
