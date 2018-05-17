#-------------------------------------------------------------------------------
#
#   PyGUI - Facilities for compatibility across Python versions
#
#-------------------------------------------------------------------------------

try:
	from __builtin__ import set
except ImportError:
	from sets import Set as set
