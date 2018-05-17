#--------------------------------------------------------------------
#
#   PyGUI - Fix py2exe to handle dynamic pywin32 module search paths
#
#--------------------------------------------------------------------

from __future__ import absolute_import
import sys

# py2exe 0.6.4 introduced a replacement modulefinder.
# This means we have to add package paths there, not to the built-in
# one.	If this new modulefinder gets integrated into Python, then
# we might be able to revert this some day.
# if this doesn't work, try import modulefinder
try:
	import py2exe.mf as modulefinder
except ImportError:
	import modulefinder
import win32com
for p in win32com.__path__[1:]:
	modulefinder.AddPackagePath("win32com", p)
for extra in ["win32com.shell"]: #,"win32com.mapi"
	__import__(extra)
	m = sys.modules[extra]
	for p in m.__path__[1:]:
		modulefinder.AddPackagePath(extra, p)
