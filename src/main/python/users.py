#!/usr/bin/python

import json
import ssl
import sys
import urllib2


def getList(url, key):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)
    if result:
        return json.load(result)


if len(sys.argv) < 3:
    print 'Usage: users.py <grafanaURL> <apiKey>'
    sys.exit(1)

url = sys.argv[1]
key = sys.argv[2]


users = getList(url + '/api/org/users', key)
items = []
for user in users:
    # print '%s %s' % (user['login'], user['email'])
    login = user['login']
    if login == 'meagar' or login == 'jsabin' or login == 'ehatch' or login == 'pulseadmin':
        pass
    else:
        print user["email"]
