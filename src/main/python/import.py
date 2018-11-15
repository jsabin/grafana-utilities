#!/usr/bin/python

import json
import os
import ssl
import sys
import urllib2

# Imports dashboards, datasources and permissions to the specified folder for the org specified by the API key.

def import_data(url, data, key):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, json.dumps(data), context=context)
    if result:
        return result


def getFolderId(url, key, folderName):
    if folderName == "General":
        return {'id': 0}

    req = urllib2.Request(url + '/api/search')
    req.add_header('Content-Type', 'application/json')
    req.add_header('authorization', 'Bearer %s' % key)
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLSv1_2)  # Note: SSLContext added in python 2.7.9
    result = urllib2.urlopen(req, context=context)

    folders = json.load(result)
    for folder in folders:
        if folder['type'] == 'dash-folder' and folder['title'] == folderName:
            return {'id': folder['id'], 'uid': folder['uid']}

    if result:
        return result


if len(sys.argv) < 5:
    print 'Usage: import.py <grafanaURL> <dashboardDir> <org> <folder> <apiKey>'
    sys.exit(1)

url = sys.argv[1]
dashboardDir = sys.argv[2]
org = sys.argv[3]
folderName = sys.argv[4]
key = sys.argv[5]

folder = getFolderId(url, key, folderName)
folderId = folder['id']
if folderName != "General" and not folderId:
    print "Could not find folder id for folder %s" % folderName
    sys.exit(1)

print 'Importing dashboards...'
dirName = '%s/%s/dashboards' % (dashboardDir, org)
for file in os.listdir(dirName):
    try:
        print 'Importing %s...' % file,
        with open(os.path.join(dirName, file), "r") as dashboard:
            dashboardJson = json.load(dashboard)
        dashboardJson["dashboard"]["id"] = "null"  # need to null out id
        dashboardJson['folderId'] = folderId

        # NOTE: if folder is "general" the folder id is not set
        response = import_data(url + "/api/dashboards/import", dashboardJson, key)
        print "success"
    except urllib2.HTTPError as e:
        print 'failed with error %s' % e.getcode()

print '\nImporting datasources...'
dirName = '%s/%s/datasources' % (dashboardDir, org)
for file in os.listdir(dirName):
    try:
        print 'Importing %s...' % file,
        with open(os.path.join(dirName, file), "r") as datasource:
            datasourceJson = json.load(datasource)

        # NOTE: if folder is "general" the folder id is not set
        response = import_data(url + "/api/datasources", datasourceJson, key)
        print "success"
    except urllib2.HTTPError as e:
        print 'failed with error %s' % e.getcode()

print '\nImporting Permissions...'
dirName = '%s/%s' % (dashboardDir, org)
try:
    with open(os.path.join(dirName, "permissions.json"), "r") as permissions:
        permissionJson = json.load(permissions)

    response = import_data(url + "/api/folders/%s/permissions" % folder['uid'], permissionJson, key)
    print "success"
except urllib2.HTTPError as e:
    print 'failed with error %s' % e.getcode()
