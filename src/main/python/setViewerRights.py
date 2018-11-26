#!/usr/bin/python

import json
import ssl
import sys
import urllib2

# Sets the rights on dashboards for the given org to Viewer.

def getList(url, key):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)
    if result:
        return json.load(result)


def import_data(url, data, key):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    req.get_method = lambda: 'PATCH'
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, json.dumps(data), context=context)
    if result:
        return result

if len(sys.argv) < 4:
    print 'Usage: setViewerRights <grafanaURL> <apiKey> <userToExclude>'
    sys.exit(1)

url = sys.argv[1]
key = sys.argv[2]
exclude = sys.argv[3]


users = getList(url + '/api/org/users', key)
items = []
for user in users:
    login = user['login']
    if login == exclude:
        pass
    else:
        print "Setting viewer rights for user %s" % user['login']
        response = import_data(url + "/api/org/users/%s" % user['userId'], {"role": "Viewer"}, key)
