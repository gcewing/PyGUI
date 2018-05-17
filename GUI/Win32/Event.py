#--------------------------------------------------------------------
#
#   PyGUI - Event - Win32
#
#--------------------------------------------------------------------

from GUI import export
from GUI.GEvents import Event as GEvent

class Event(GEvent):

	def _platform_modifiers_str(self):
		return ""

export(Event)
