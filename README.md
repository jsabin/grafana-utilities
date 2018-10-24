# Grafana Utilities


## Delete
Deletes all dashboards in an organization.

`Usage: delete <grafanaURL> <apiKey`

##### Example

`delete.py http://myServer.com eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk`


## Export
Exports dashboards, datasources, and permissions. 

Exports data given an API key to the local file system for use by the import utility. Data is stored by organization name.

`Usage: export.py <grafanaURL> <folder> <apiKey>`

##### Example

`export.py http://myServer.com myFolder eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk`
 

## Import
Imports dashboards, datasources, and permissions.

`Usage: import.py <grafanaURL> <dashboardDir> <org> <folder> <apiKey>`

##### Example

`import.py http://myServer.com dashboards myOrg myFolder eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk`


Tested with Grafana 5.2.x



