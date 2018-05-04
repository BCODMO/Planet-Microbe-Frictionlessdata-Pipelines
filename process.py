from datapackage import Package
from goodtables import validate
import os

if __name__ == '__main__':
  url = 'https://www.bco-dmo.org/project/2101/datapackage.json'
  download_dir = './HOT-project'
  handleDataPackage(path=url, root_directory=download_dir)
  
# @param string path
#   either a local file or a URL
def handleDataPackage(path='', root_directory='', save_pkg_file=True):
  package = Package(path)
  if package.valid:

    if save_pkg_file:
      package_filename = os.path.join(root_directory, os.path.basename(path))
      package.save(target=package_filename)

    for i in range(len(package.resource_names)):
      handleResource(package.get_resource(package.resource_names[i]), root_directory)

def handleResource(resource, root_directory):
  if resource.valid:
    if 'application/vnd.datapackage+json' == resource.descriptor['mediatype']:
      handleDataPackageResource(resource, root_directory)
    else:
      handleDataResource(resource, root_directory)

def handleDataPackageResource(resource, directory):
  print(resource.source)
  # order_fields ignores order mismatch with b/w source and schema
  report = validate(resource.source, order_fields=True)
  if report['valid']:
    print ('Good Tables: Valid')
  else:
    print('Good Tables: ' + str(report['error-count']) + ' errors')
    for i in range(len(report['tables'])):
      print('ERRORS in ' + report['tables'][i]['source'])
      for j in range(len(report['tables'][i]['errors'])):
        print(' - ' + report['tables'][i]['errors'][j]['message'])

  resource_directory = os.path.join(directory, resource.descriptor['name'])
  dir_file = downloadResource(resource, resource_directory, os.path.basename(resource.source))
  print('Downloaded Data Package: ' + dir_file)
  handleDataPackage(path=dir_file, root_directory=resource_directory, save_pkg_file=False)

def handleDataResource(resource, directory):
  resource_filename = resource.descriptor['name']
  if 'format' in resource.descriptor.keys():
    resource_filename += '.' + resource.descriptor['format']
  dir_file = downloadResource(resource, directory, resource_filename)
  print('Downloaded Data Resource: ' + dir_file)

def downloadResource(resource, directory, filename):
  if not os.path.exists(directory):
    os.makedirs(directory)
  if not os.path.exists(directory):
    raise Exception(directory + ' does not exist and could not be created')

  dir_file = os.path.join(directory, filename)
  print('Writing file: ' + dir_file)

  socket_file = resource.raw_iter(stream=True)
  data = socket_file.read()
  with open(dir_file, 'wb') as file:
    file.write(data)

  # check if the resource provided a bytesize
  if 'bytes' in resource.descriptor.keys():
    downloaded_bytesize = os.path.getsize(dir_file)
    if resource.descriptor['bytes'] != downloaded_bytesize:
      raise Exception('Downloaded resource does not have the same byte size[' + downloaded_bytesize + ' bytes] as reported in the data package[' + resource.descriptor['bytes'] + ' bytes]: ' + dir_file)
    else:
      print('Data package did not report a byte size to verify')

  # check the hash of the resource
  #if 'hash' in resource.descriptor.keys():
  #  downloaded_md5 =  hashlib.md5(dir_file)
  #  if resource.descriptor['hash'] != downladed_bytesize:
  #    raise Exception('Downloaded resource does not have the same MD5 hash[' + downloaded_md5 + '] as reported in the data package[' + resource.descriptor['hash'] + ']: ' + dir_file)
  #  else:
  #    print('Data package did not report a hash to verify')

  return dir_file

