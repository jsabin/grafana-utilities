#!/usr/bin/python

import ssl
import urllib2
import json
import sys


# Lists datasources used by dashboards

def get_datasource(url, key, datasourceId):
    req = urllib2.Request(
        "%s/api/datasources/%s" % (url, datasourceId))
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)
    if result:
        return result


def getList(url, key):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)
    if result:
        return json.load(result)

def get_dashboard(url, key, dashboard):
    req = urllib2.Request(
        "%s/api/dashboards/%s" % (url, dashboard))
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)
    if result:
        return result


if len(sys.argv) < 3:
    print 'Usage: used-dashboards.py <grafanaURL> <apiKey>'
    sys.exit(1)

url = sys.argv[1]
key = sys.argv[2]

datasourcesJson = getList(url + '/api/datasources', key)
datasources = set()
for datasource in datasourcesJson:
    datasources.add(datasource['name'])

usedDatasources = set()
dashboards = getList(url + '/api/search?query=&', key)
for dashboard in dashboards:
    if dashboard['type'] == 'dash-db':
        dashboardJson = json.load(get_dashboard(url, key, dashboard['uri']))

        print '%s:' % dashboard['title'],
        dashDatasources = set()

        if 'rows' in dashboardJson['dashboard']:
            rows = dashboardJson['dashboard']['rows']
            for row in rows:
                if 'panels' in row:
                    panels = row['panels']
                    for panel in panels:
                        if 'datasource' in panel:
                            src = panel['datasource']
                            if not src or src == 'None' or src[:1] == '$':
                                pass
                            else:
                                dashDatasources.add(src)

        usedDatasources = usedDatasources | dashDatasources
        for datasource in dashDatasources:
            print "\t%s " % datasource,
        print

print '------------------------------------'
print 'Datasources not used:'
for datasource in datasources.difference(usedDatasources):
    print datasource
