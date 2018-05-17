#
#   PyGUI - Resources - Generic
#

import os

resource_path = []
resource_cache = {}

class ResourceNotFoundError(ValueError):

	def __init__(self, name, type, path):
		name = _append_type(name, type)
		ValueError.__init__(self, "Resource %r not found in %s" % (name, path))

def _append_type(name, type):
	if type:
		name = "%s.%s" % (os.path.splitext(name)[0], type)
	return name	

def _add_directory_path(dir, up = 0):
	#  Add the given directory to the resource path if it exists.
	dir = os.path.abspath(dir)
	while up > 0:
		dir = os.path.dirname(dir)
		up -= 1
	resdir = os.path.join(dir, "Resources")
	#print "GUI.Resources: Checking for directory", repr(resdir) ###
	if os.path.isdir(resdir):
		resource_path.insert(0, resdir)

def _add_file_path(file, up = 0):
	#  Add the directory containing the given file to the resource path.
	#print "GUI.Resources: Adding path for file", repr(file) ###
	dir = os.path.dirname(os.path.abspath(file))
	_add_directory_path(dir, up)

def _add_module_path(module, up = 0):
	#  Add the directory containing the given module to the resource path.
	if hasattr(module, '__file__'):
		_add_file_path(module.__file__, up)

def lookup_resource(name, type = None):
	"""
	Return the full pathname of a resource given its relative name
	using '/' as a directory separator. If a type is specified, any
	dot-suffix on the name is replaced with '.type'. Returns None if
	no matching file is found on the resource search path.
	"""
	name = _append_type(name, type)
	relpath = os.path.join(*name.split("/"))
	for dir in resource_path:
		path = os.path.join(dir, relpath)
		if os.path.exists(path):
			return path
	return None

def find_resource(name, type = None):
	"""
	Returns the full pathname of a resource as per lookup_resource(), but
	raises ResourceNotFoundError if the resource is not found.
	"""
	path = lookup_resource(name, type)
	if not path:
		raise ResourceNotFoundError(name, type, resource_path)
	return path

def get_resource(loader, name, type = None, default = None, **kwds):
	"""
	Find a resource and load it using the specified loader function.
	The loader is called as: loader(path, **kwds) where path is the full
	pathname of the resource. The loaded resource is cached, and subsequent
	calls referencing the same resource will return the cached value.
	If the resource is not found, the specified default is returned if any,
	otherwise ResourceNotFoundError is raised.
	"""
	path = lookup_resource(name, type)
	if path:
		result = resource_cache.get(path)
		if result is None:
			result = loader(path, **kwds)
			resource_cache[path] = result
	else:
		if default is not None:
			result = default
		else:
			raise ResourceNotFoundError(name, type, resource_path)
	return result
