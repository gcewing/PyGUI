#
#   Python GUI - Containers - PyObjC version
#

from AppKit import NSView
from GUI.Utils import PyGUI_Flipped_NSView
from GUI import export
from GUI.GContainers import Container as GContainer

class Container(GContainer):
	#  _ns_inner_view   NSView   Containing NSView for subcomponents
	
#	def __init__(self, _ns_view, **kwds):
#		GContainer.__init__(self, _ns_view = _ns_view, **kwds)
	
#	def destroy(self):
#		#print "Container.destroy:", self ###
#		GContainer.destroy(self)
#		#print "Container.destroy: breaking inner link to", self._ns_inner_view ###

	def _add(self, comp):
		GContainer._add(self, comp)
		self._ns_inner_view.addSubview_(comp._ns_view)

	def _remove(self, comp):
		GContainer._remove(self, comp)
		comp._ns_view.removeFromSuperview()

#------------------------------------------------------------------------------

export(Container)
