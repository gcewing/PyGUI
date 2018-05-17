#--------------------------------------------------------------------
#
#   PyGUI - Generic - Global variables and functions
#
#--------------------------------------------------------------------

import os, sys

_main_file_name = os.path.basename(sys.argv[0])
application_name = os.path.splitext(_main_file_name)[0]

_application = None

def application():
	"""Returns the global Application object. Creates a default one if needed."""
	global _application
	if not _application:
		from GUI import Application
		_application = Application()
	return _application

def run():
	"""Runs the application, retaining control until the application is quit."""
	application().run()

