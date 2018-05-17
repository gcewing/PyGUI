#
#   Python GUI - Scrollable Views - Gtk
#

from gi.repository import Gtk
from GUI.Scrollables import Scrollable, gtk_scrollbar_breadth
from GUI.GScrollableViews import ScrollableView as GScrollableView, \
	default_extent, default_line_scroll_amount
from GUI.Geometry import offset_rect_neg

class ScrollableView(GScrollableView, Scrollable):

	def __init__(self, extent = default_extent,
			line_scroll_amount = default_line_scroll_amount,
			**kwds):
		gtk_scrolled_window = Gtk.ScrolledWindow()
		gtk_scrolled_window.show()
		GScrollableView.__init__(self, _gtk_outer = gtk_scrolled_window,
			extent = extent, line_scroll_amount = line_scroll_amount, **kwds)
	
	#
	#   Properties
	#
	
	def get_content_width(self):
		w = self._size[0]
		if self.hscrolling:
			w -= gtk_scrollbar_breadth
		return w
	
	def get_content_height(self):
		h = self._size[1]
		if self.vscrolling:
			h -= gtk_scrollbar_breadth
		return h
	
	def get_content_size(self):
		return self.content_width, self.content_height
	
	def set_content_size(self, size):
		w, h = size
		d = gtk_scrollbar_breadth
		if self.hscrolling:
			w += d
		if self.vscrolling:
			h += d
		self.size = (w, h)

	def get_extent(self):
		return self._gtk_inner_widget.get_size()
	
	def set_extent(self, (w, h)):
		self._gtk_inner_widget.set_size(w, h)

	def get_scroll_offset(self):
		hadj, vadj = self._gtk_adjustments()
		return int(hadj.get_value()), int(vadj.get_value())

	def set_scroll_offset(self, (x, y)):
		hadj, vadj = self._gtk_adjustments()
		hadj.set_value(min(float(x), hadj.get_upper() - hadj.get_page_size()))
		vadj.set_value(min(float(y), vadj.get_upper() - vadj.get_page_size()))

	def get_line_scroll_amount(self):
		hadj, vadj = self._gtk_adjustments()
		return hadj.get_step_increment(), vadj.get_step_increment()
	
	def set_line_scroll_amount(self, (dx, dy)):
		hadj, vadj = self._gtk_adjustments()
		hadj.set_step_increment(float(dx)) # Amazingly, ints are not
		vadj.set_step_increment(float(dy)) # acceptable here.
	
	def invalidate_rect(self, rect):
		GScrollableView.invalidate_rect(self,
			offset_rect_neg(rect, self.scroll_offset))
	
	#
	#		Internal
	#

	def _gtk_adjustments(self):
		gtk_widget = self._gtk_inner_widget
		hadj = gtk_widget.get_hadjustment()
		vadj = gtk_widget.get_vadjustment()
		return hadj, vadj

	def _gtk_prepare_cairo_context(self, context):
		x, y = self.scroll_offset
		context.translate(-x, -y)
