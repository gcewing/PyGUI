#--------------------------------------------------------------------
#
#   PyGUI - DrawableContainer - Generic
#
#--------------------------------------------------------------------

from GUI.Geometry import rect_sized
from GUI import Container
from GUI import ViewBase
from GUI.Printing import Printable

default_size = (100, 100)

class DrawableContainer(ViewBase, Container, Printable):

	#
	#		Construction and destruction
	#

	def __init__(self, **kwds):
		Container.__init__(self, **kwds)
		ViewBase.__init__(self)
	
	def destroy(self):
		ViewBase.destroy(self)
		Container.destroy(self)
		
	def setup_menus(self, m):
		ViewBase.setup_menus(self, m)
		Container.setup_menus(self, m)

	def viewed_rect(self):
		"""Return the rectangle in local coordinates bounding the currently
		visible part of the extent."""
		return rect_sized((0, 0), self.size)
	
	def with_canvas(self, proc):
		"""Call the procedure with a canvas suitable for drawing in this
		view. The canvas is only valid for the duration of the call, and
		should not be retained beyond it."""
		raise NotImplementedError
	
	def update(self):
		"""Redraw invalidated regions immediately, without waiting for a
		return to the event loop."""
		raise NotImplementedError

	def get_print_extent(self):
		return self.content_size

	def _draw_background(self, canvas, clip_rect):
		return clip_rect

	#
	#		Callbacks
	#

	def draw(self, canvas, rect):
		"""Called when the view needs to be drawn. The rect is the bounding
		rectangle of the region needing to be drawn. The default implementation
		does nothing."""
		pass
