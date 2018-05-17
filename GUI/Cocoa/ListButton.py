#--------------------------------------------------------------
#
#   PyGUI - Pop-up list control - Cocoa
#
#--------------------------------------------------------------

from AppKit import NSPopUpButton
from GUI import export
from GUI.GListButtons import ListButton as GListButton
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler, \
	ns_set_action, ns_size_to_fit

class ListButton(GListButton):

	_ns_handle_mouse = True

	def __init__(self, **kwds):
		titles, values = self._extract_initial_items(kwds)
		self._titles = titles
		self._values = values
		frame = ((0, 0), (100, 20))
		ns = PyGUI_NSPopUpButton.alloc().initWithFrame_pullsDown_(frame, False)
		ns.pygui_component = self
		ns_set_action(ns, 'doAction:')
		self._ns_update_items(ns)
		ns_size_to_fit(ns)
		GListButton.__init__(self, _ns_view = ns, **kwds)
	
	def _update_items(self):
		self._ns_update_items(self._ns_view)
	
	def _ns_update_items(self, ns):
		ns.removeAllItems()
		ns.addItemsWithTitles_(self._titles)
	
	def _get_selected_index(self):
		return self._ns_view.indexOfSelectedItem()
	
	def _set_selected_index(self, i):
		self._ns_view.selectItemAtIndex_(i)

#--------------------------------------------------------------

class PyGUI_NSPopUpButton(NSPopUpButton, PyGUI_NS_EventHandler):
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']

export(ListButton)
