#------------------------------------------------------------------------------
#
#		Python GUI - Frames - Cocoa
#
#------------------------------------------------------------------------------

from GUI.GFrames import Frame as GFrame
from GUI import export
from GUI.Utils import NSMultiClass
from GUI.Utils import PyGUI_NS_EventHandler, PyGUI_Flipped_NSView

class Frame(GFrame):

	def __init__(self, **kwds):
		ns_view = PyGUI_Frame.alloc().initWithFrame_(((0, 0), (100, 100)))
		ns_view.pygui_component = self
		GFrame.__init__(self, _ns_view = ns_view, **kwds)

#------------------------------------------------------------------------------

class PyGUI_Frame(PyGUI_Flipped_NSView, PyGUI_NS_EventHandler):
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']

export(Frame)
