#-------------------------------------------------------------------------
#
#   PyGUI - Distutils Setup Script
#
#-------------------------------------------------------------------------

import os, sys
from glob import glob
from distutils.core import setup
#from distutils.extension import Extension
from distutils.sysconfig import get_python_lib
from distutils_extensions import pygui_build_py

#
#   PyPI Classifiers
#

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Environment :: MacOS X :: Cocoa
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: Developers
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
Operating System :: Microsoft :: Windows
Programming Language :: Python
Topic :: Software Development :: User Interfaces
""" #Programming Language :: Python :: 3

#
#   Python 3 Conversion
#

if sys.version_info >= (3,0): #automatically convert to Python 3 syntax while installing
#   #build_py_2to3 now imported in distutils_extensions
#  	try:
#  		from distutils.command.build_py import build_py_2to3 as build_py
#  	except ImportError:
#  		raise ImportError("build_py_2to3 not found in distutils - it is required for Python 3.x")
##		# exclude fixers that break already compatible code
##		from lib2to3.refactor import get_fixers_from_package
##		fixers = get_fixers_from_package('lib2to3.fixes')
##		for skip_fixer in ['import']:
##			fixers.remove('lib2to3.fixes.fix_' + skip_fixer)
##		build_py.fixer_names = fixers
	print('Installing for Python3')
#  else: # install Python 2.x version
#  	from distutils.command.build_py import build_py

#
#   Installation parameters
#

cmd_class = {'build_py': pygui_build_py}
ext_modules = []

version = '<version not found>'
version_file = os.path.join("GUI", "Version.py") 
# get accurate version sring by running Version.py
exec(compile(open(version_file,'r').read(), version_file, 'exec'))

#
#   Find which implementation to install
#

plat = sys.platform
if plat.startswith("darwin"):
	platdir = "Cocoa"
elif plat.startswith("linux"):
	platdir = "Gtk"
elif plat.startswith("win"):
	platdir = "Win32"
else:
	sys.stderr.write(
		"Don't know which backend to install for platform '%s'.\n"
			% plat)
	sys.exit(1)
	
sys.stdout.write("Installing backend %s\n" % platdir)

#
#   Pyrex
#

#have_pyrex = 0

#try:
#	import Pyrex.Distutils
#	print "Pyrex available"
#	have_pyrex = 1
#	cmdclass = {'build_ext': Pyrex.Distutils.build_ext}
#except ImportError:
#	pass

#if sys.platform == "darwin":
#	if have_pyrex:
#		agl_source = "GUI/Mac/AGL.pyx"
#	else:
#		agl_source = "GUI/Mac/AGL.c"
#	agl_module = Extension("GUI.Mac.AGL", [agl_source], 
#		include_dirs = ["/System/Library/Frameworks/AGL.framework/Headers"],
#		extra_link_args = ["-Wl,-w", "-framework", "AGL", "-framework", "Carbon"])
#	ext_modules.append(agl_module)

#
#   Setup
#

setup(
	cmdclass = cmd_class,
	name = "PyGUI",
	version = version,
	description = "Pythonic Cross-Platform GUI Framework",
	author = "Gregory Ewing",
	author_email = "greg.ewing@canterbury.ac.nz",
	url = "http://www.cosc.canterbury.ac.nz/greg.ewing/python_gui",
	#download_url=DOWNLOAD_URL,
	long_description = open('README.txt').read(),
	platforms = ["Linux", "MacOS X", "Windows"],
	packages = ["GUI"],
	package_subdirs = {"GUI": ["Generic", platdir]},
	package_data = {"GUI": [os.path.join("Resources", "*", "*")]},
	ext_modules = ext_modules,
	#maintainer=MAINTAINER,
	#maintainer_email=MAINTAINER_EMAIL,
	keywords = 'GUI Cross-Platform',
	license = 'This is free software. You are welcome to use it however you want.'
)
