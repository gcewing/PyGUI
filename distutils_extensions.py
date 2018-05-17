#------------------------------------------------------------------------
#
#   PyGUI - Distutils hackery
#
#------------------------------------------------------------------------

import os, sys
from glob import glob
from distutils.dist import Distribution

if sys.version_info >= (3, 0):
	try:
		from distutils.command.build_py import build_py_2to3 as build_py
	except ImportError:
		raise ImportError("build_py_2to3 not found in distutils - it is required for Python 3.x")
else:
	from distutils.command.build_py import build_py

#------------------------------------------------------------------------

class pygui_build_py(build_py):
	"""
	An extension of the distutils build_py command that supports
	gathering .py files for a package from multiple source directories.
	
	It provides a new option 'package_subdirs' that is a mapping from
	a package name to a list of directory paths:
	
	package_subdirs = {'package_name': ['source_dir', ...], ...}
	
	The directory paths are interpreted relative to the primary source
	directory for the package. In addition to .py files from the primary
	source directory, any .py files from the specified directories will be
	copied into the package during installation.
	"""
	
	Distribution.package_subdirs = {}
	
	def initialize_options(self):
		build_py.initialize_options(self)
		self.package_subdirs = {}
	
	def finalize_options(self):
		build_py.finalize_options(self)
		self.package_subdirs = self.distribution.package_subdirs
	
	def find_package_modules(self, package, package_dir):
		#print "distutils_extensions: Searching subdirectories of package", repr(package) ###
		modules = build_py.find_package_modules(self, package, package_dir)
		subdirs = self.package_subdirs.get(package, ())
		for subdir in subdirs:
			#print "Looking in subdir", repr(subdir), "of", repr(package_dir) ###
			module_files = glob(os.path.join(package_dir, subdir, "*.py"))
			for f in module_files:
				module = os.path.splitext(os.path.basename(f))[0]
				#print "Found module", repr(module), "in", repr(f) ###
				modules.append((package, module, f))
		return modules
