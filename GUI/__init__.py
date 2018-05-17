#--------------------------------------------------------------------
#
#   PyGUI - Top level package initialisation
#
#--------------------------------------------------------------------

import sys, types

#  The first item of each of the following pairs is the name of a module
#  to try to import. If the import is successful, the platform-dependent
#  directory named by the second item is used.

_versions = [
	("objc", "Cocoa"),
	("nt", "Win32"),
	("gi.repository.Gtk", "GtkGI"),
	("gtk", "Gtk"),
]

#  
#  The following function exports a class or function from a submodule in
#  such a way that it appears to have been defined directly at the top
#  level of the package. By giving the submodule that defines the class the
#  same name as the class, this provides an autoloading facility that is
#  friendly to application bundling tools.
#

_preserve = []  # Keeps references to replaced modules so they aren't cleared

def export(obj):
	qname = "%s.%s" % (__name__, obj.__name__)
	obj.__module__ = __name__
	mod = sys.modules[qname]
	_preserve.append(mod)
	sys.modules[qname] = obj

#
#  The environment variable PYGUI_IMPLEMENTATION may be set to the
#  name of one of the platform-dependent directories to force that
#  implementation to be used. This can be useful if more than one
#  PyGUI implementation is usable on your setup.
#

from os import environ as _env
_platdir = _env.get("PYGUI_IMPLEMENTATION")
if not _platdir:
	for _testmod, _platdir in _versions:
		try:
			__import__(_testmod)
			break
		except ImportError:
			continue
	else:
		raise ImportError("Unable to find an implementation of PyGUI for this installation")

if _env.get("PYGUI_IMPLEMENTATION_DEBUG"):
	sys.stderr.write("PyGUI: Using implementation: %s\n" % _platdir)

#
#  Append the chosen platform-dependent directory to the search
#  path for submodules of this package.
#

from os.path import join as _join
_here = __path__[0]
__path__.append(_join(_here, _platdir))
__path__.append(_join(_here, "Generic"))

#
#  Import global functions
#

from GUI.Globals import application, run
from GUI.Colors import rgb

#
#  Set up initial resource search path
#

from GUI import Resources
Resources._add_file_path(__file__)
_main_dir = sys.path[0]
Resources._add_directory_path(_main_dir)
Resources._add_directory_path(_main_dir, 1)
#import __main__
#Resources._add_module_path(__main__)
#Resources._add_module_path(__main__, 1)
#print "GUI: resource_path =", Resources.resource_path ###

#
#   Perform global initialisation
#

import GUI.Application
