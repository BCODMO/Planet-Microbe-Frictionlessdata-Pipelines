from datapackage import Package

package = Package('https://www.bco-dmo.org/project/2101/datapackage.json')

for i in range(len(package.resource_names)):
    print(package.resource_names[i])
    resource = package.get_resource(package.resource_names[i])
    print(resource.raw_read())
