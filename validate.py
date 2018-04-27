from datapackage import Package
import os

package = Package('https://www.bco-dmo.org/project/2101/datapackage.json')
if package.valid:
  for i in range(len(package.resource_names)):
    print(package.resource_names[i])
    resource = package.get_resource(package.resource_names[i])
    if resource.valid:
      socket_file = resource.raw_iter(stream=True)
      file_data = socket_file.read()
      if not os.path.exists(package.resource_names[i]):
        os.makedirs(package.resource_names[i])
      filename = os.path.join(package.resource_names[i], os.path.basename(resource.source))
      with open(filename, 'wb') as ofile:
        ofile.write(file_data)
      print('Wrote: ' + filename)
