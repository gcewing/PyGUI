#-------------------------------------------------------------------------------
#
#		Python GUI - Scrollable objects mixin - Cocoa
#
#-------------------------------------------------------------------------------

from GUI import export
from GUI.GScrollableBases import ScrollableBase as GScrollableBase

class ScrollableBase(GScrollableBase):

	def get_hscrolling(self):
		return self._ns_view.hasHorizontalScroller()
	
	def set_hscrolling(self, value):
		self._ns_view.setHasHorizontalScroller_(value)
	
	def get_vscrolling(self):
		return self._ns_view.hasVerticalScroller()
	
	def set_vscrolling(self, value):
		self._ns_view.setHasVerticalScroller_(value)
	
export(ScrollableBase)
