#
#   Python GUI - Labels - Generic
#

from GUI.Properties import overridable_property
from GUI import Control

class Label(Control):
	"""A piece of static text for labelling items in a window."""
	
	_default_tab_stop = False
	
	text = overridable_property('text')
	
