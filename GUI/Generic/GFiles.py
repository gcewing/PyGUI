#
#		Python GUI - File references and types - Generic
#
#		Classes for dealing with file references and file types
#		in as platform-independent a manner as possible.
#
#		In this view of things, a file reference consists
#		of two parts:
#
#			 1) A directory reference, whose nature is
#					platform-dependent,
#
#			 2) A name.
#

import os
from GUI.Properties import Properties, overridable_property

class FileRef(Properties):
	"""A FileRef represents a file system object in a platform-independent way.
	It consists of two parts, a directory specification and the name of an
	object within that directory. The directory specification always refers
	to an existing directory, but the named object may or may not exist.
	
	Constructors:
		FileRef(dir = DirRef or path, name = string)
		FileRef(path = string)
	"""

	dir = overridable_property('dir', "DirRef representing the parent directory.")
	name = overridable_property('name', "Name of the object within the parent directory.")
	path = overridable_property('path', "Full pathname of the object.")

	_dir = None		# DirRef representing the parent directory
	_name = None	# Name, including type suffix if any
	
	#
	#   Constructor
	#
	
	def __init__(self, dir = None, name = None, path = None):
		if dir and name and not path:
			if not isinstance(dir, DirRef):
				dir = DirRef(dir)
		elif path and not (dir or name):
			dirpath, name = os.path.split(path)
			dir = DirRef(path = dirpath)
		else:
			raise TypeError("Invalid argument combination to FileRef constructor")
		self._dir = dir
		self._name = name

	#
	#		Properties
	#

	def get_dir(self):
		return self._dir

	def get_name(self):
		"Return the name of the file."
		return self._name

	def get_path(self):
		return os.path.join(self._dir.path, self._name)

	#
	#		Methods
	#

	def open(self, mode, file_type = None):
		"""Open as a file with the given mode and return a file object. On
		platforms which have file-type metadata (e.g. Macintosh), if the
		mode contains 'w' and a file_type is specified, the newly-created
		file will be given the specified type."""
		f = open(self.path, mode)
		if "w" in mode and file_type:
			self._set_type(file_type)
		return f
	
	def mkdir(self):
		"""Create a directory with the name and parent directory specified
		by this FileRef. Returns a DirRef for the created directory."""
		return DirRef(os.mkdir(self.path))
	
	def _set_type(self, file_type):
		#  Platforms which have file-type metadata (e.g. Macintosh) use this
		#  to set the type of a file.
		pass

	def __str__(self):
		return "FileRef(%r,%r)" % (self.dir.path, self.name)

#-------------------------------------------------------------------------

class DirRef(Properties):
	"""A DirRef is an object representing a directory in the
	file system. Its representation is completely platform
	dependent.
	
	Constructor:
		DirRef(path = string)
	"""

	_path = None

	path = overridable_property('path', "Full pathname of the directory.")
	
	def __init__(self, path):
		self._path = path

	def get_path(self):
		return self._path

	def __str__(self):
		return "DirRef(%r)" % self.path

#-------------------------------------------------------------------------

class FileType(Properties):
	"""A FileType is a multi-platform representation of a file type."""
	
	_name = None
	_suffix = None
	_mac_creator = None
	_mac_type = None
	_mac_force_suffix = True
	
	name = overridable_property('name', "Human-readable description of the file type")
	suffix = overridable_property('suffix', "Filename suffix (without dot)")
	mac_creator = overridable_property('mac_creator', "Macintosh 4-character creator code")
	mac_type = overridable_property('mac_type', "Macintosh 4-character type code")
	mac_force_suffix = overridable_property('mac_force_suffix', "Enforce filename suffix on MacOSX")
	
	def get_name(self):
		return self._name
	
	def set_name(self, x):
		self._name = x
	
	def get_suffix(self):
		return self._suffix
	
	def set_suffix(self, x):
		self._suffix = x
	
	def get_mac_creator(self):
		return self._mac_creator
	
	def set_mac_creator(self, x):
		self._mac_creator = x

	def get_mac_type(self):
		return self._mac_type
	
	def set_mac_type(self, x):
		self._mac_type = x
	
	def get_mac_force_suffix(self):
		return self._mac_force_suffix
	
	def set_mac_force_suffix(self, x):
		self._mac_force_suffix = x

	def _matches(self, name, mac_type):
		#  Return true if the given name or type code matches that of
		#  this file type.
		this_mac_type = self._mac_type
		this_suffix = self._suffix
		if this_mac_type and mac_type == this_mac_type:
			return True
		#  Allow generic text files to match typeless files for MacOSX
		if not this_suffix and this_mac_type == "TEXT" and mac_type == "\0\0\0\0":
			return True
		if this_suffix and _matches_suffix(name, this_suffix):
			return True
		return False
	
	def _add_suffix(self, name):
		#  Force the given name to have the appropriate suffix for this file
		#  type. Platforms which have other means of representing file types
		#  (e.g. Macintosh) may override this.
		suffix = self._suffix
		if suffix and not _matches_suffix(name, suffix):
			name = "%s.%s" % (name, suffix)
		return name
	
#-------------------------------------------------------------------------

def _matches_suffix(name, suffix):
	#  Test case-insensitively whether the given filename has
	#  the given suffix.
	return name.lower().endswith("." + suffix.lower())
