#-------------------------------------------------------------------------------
#
#		Python GUI - Scrollable objects mixin - Generic
#
#-------------------------------------------------------------------------------

from GUI.Properties import overridable_property

class ScrollableBase(object):
	"""Mixin for components that can be configured to have scroll bars."""

	scrolling = overridable_property('scrolling',
		"String containing 'h' for horizontal and 'v' for vertical scrolling.")
	
	hscrolling = overridable_property('hscrolling',
		"True if horizontal scrolling is enabled.")
	
	vscrolling = overridable_property('vscrolling',
		"True if vertical scrolling is enabled.")
	
	def get_scrolling(self):
		chars = []
		if self.hscrolling:
			chars.append('h')
		if self.vscrolling:
			chars.append('v')
		return ''.join(chars)
	
	def set_scrolling(self, value):
		self.hscrolling = 'h' in value
		self.vscrolling = 'v' in value

