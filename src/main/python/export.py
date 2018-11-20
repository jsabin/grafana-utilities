#!/usr/bin/python

import json
import ssl
import sys
import urllib2
import os
import errno


# Exports Dashboards, Datasources, and org permissions


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


def getOrgName(url, key):
    req = urllib2.Request(
        "%s/api/org" % url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)
    if result:
        return json.load(result)['name']


def removeProperties(dashboard):
    if '.overwrite' in dashboard:
        del dashboard['.overwrite']
    if '.dashboard.version' in dashboard:
        del dashboard['.dashboard.version']
    if '.meta.created' in dashboard:
        del dashboard['.meta.created']
    if '.meta.createdBy' in dashboard:
        del dashboard['.meta.createdBy']
    if '.meta.updated' in dashboard:
        del dashboard['.meta.updated']
    if '.meta.updatedBy' in dashboard:
        del dashboard['.meta.updatedBy']
    if '.meta.expires' in dashboard:
        del dashboard['.meta.expires']
    if '.meta.version' in dashboard:
        del dashboard['.meta.version']


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def convertToPermissionField(role):
    if role.lower() == "viewer":
        return 1
    elif role.lower() == 'editor':
        return 2
    elif role.lower() == 'admin':
        return 4
    else:
        raise Exception('Invalid permission role %s' % role)


def setDefaultDatasource(dict):
    if 'datasource' in dict and not dict['datasource']:
        dict['datasource'] = defaultDataSource
    return dict


if len(sys.argv) < 4:
    print 'Usage: export.py <grafanaURL> <folder> <apiKey>'
    sys.exit(1)

url = sys.argv[1]
folder = sys.argv[2]
key = sys.argv[3]

orgName = getOrgName(url, key)
folder = os.path.join(folder, orgName)

print '\nExporting Datasources'
defaultDataSource = ''
datasources = getList(url + '/api/datasources', key)
for datasource in datasources:
    print datasource['name']
    datasourceJson = json.load(get_datasource(url, key, datasource['id']))
    if datasourceJson['isDefault']:
        defaultDataSource = datasourceJson['name']

    outDir = os.path.join(folder, "datasources", )
    mkdir(outDir)
    with open(os.path.join(outDir, datasource['name'] + '.json'), "w") as outFile:
        json.dump(datasourceJson, outFile, indent=4)

dashboards = getList(url + '/api/search?query=&', key)
print '\nExporting dashboards...'
for dash in dashboards:
    if dash['type'] == 'dash-db' and len(dash['title']) > 0:
        dashName = dash['title']
        print dashName
        dashboardJson = json.load(get_dashboard(url, key, dash['uri']), object_hook=setDefaultDatasource)
        removeProperties(dashboardJson)

        # If using the default datasource (null) then set to the name of default. Because this could be different than the default in the org moving to

        outDir = os.path.join(folder, "dashboards")
        mkdir(outDir)
        filename = '%s.json' % dashName
        filename = filename.replace("/", "-") # Replace slashes with dash
        with open(os.path.join(outDir, filename), "w") as outFile:
            json.dump(dashboardJson, outFile, indent=4)

print '\nExporting Permissions'
users = getList(url + '/api/org/users', key)
items = []
for user in users:
    print user['login']
    permission = convertToPermissionField(user['role'])
    items.append({'userId': user['userId'], 'permission': permission})

with open(os.path.join(folder, 'permissions.json'), "w") as outFile:
    json.dump({'items': items}, outFile, indent=4)
