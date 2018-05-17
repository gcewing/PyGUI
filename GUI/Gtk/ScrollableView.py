#
#   Python GUI - Scrollable Views - Gtk
#

import gtk
from GUI import export
from GUI import Scrollable
from GUI.GScrollableViews import ScrollableView as GScrollableView, \
	default_extent, default_line_scroll_amount, default_scrolling

class ScrollableView(GScrollableView, Scrollable):

	def __init__(self, extent = default_extent,
			line_scroll_amount = default_line_scroll_amount,
			scrolling = default_scrolling,
			**kwds):
		gtk_scrolled_window = gtk.ScrolledWindow()
		gtk_scrolled_window.show()
		GScrollableView.__init__(self, _gtk_outer = gtk_scrolled_window,
			extent = extent, line_scroll_amount = line_scroll_amount,
			scrolling = scrolling)
		self.set(**kwds)
	
	#
	#   Properties
	#
	
	def get_border(self):
		return self._gtk_outer_widget.get_shadow_type() <> gtk.SHADOW_NONE
	
	def set_border(self, x):
		if x:
			s = gtk.SHADOW_IN
		else:
			s = gtk.SHADOW_NONE
		self._gtk_outer_widget.set_shadow_type(s)
	
	def get_content_width(self):
		w = self._size[0]
		if self.hscrolling:
			w -= self.gtk_scrollbar_breadth
		if self.border:
			w -= 2 * self.gtk_border_thickness[0]
		return w
	
	def get_content_height(self):
		h = self._size[1]
		if self.vscrolling:
			h -= self.gtk_scrollbar_breadth
		if self.border:
			h -= 2 * self.gtk_border_thickness[1]
		return h
	
	def get_content_size(self):
		return self.content_width, self.content_height
	
	def set_content_size(self, size):
		w, h = size
		d = self.gtk_scrollbar_breadth
		if self.hscrolling:
			w += d
		if self.vscrolling:
			h += d
		if self.border:
			b = self.gtk_border_thickness
			w += 2 * b[0]
			h += 2 * b[1]
		self.size = (w, h)
	
	def get_extent(self):
		return self._gtk_inner_widget.get_size()
	
	def set_extent(self, (w, h)):
		self._gtk_inner_widget.set_size(int(round(w)), int(round(h)))

	def get_scroll_offset(self):
		hadj, vadj = self._gtk_adjustments()
		return int(hadj.value), int(vadj.value)
	
	def set_scroll_offset(self, (x, y)):
		hadj, vadj = self._gtk_adjustments()
		hadj.set_value(min(float(x), hadj.upper - hadj.page_size))
		vadj.set_value(min(float(y), vadj.upper - vadj.page_size))
	
	def get_line_scroll_amount(self):
		hadj, vadj = self._gtk_adjustments()
		return hadj.step_increment, vadj.step_increment
	
	def set_line_scroll_amount(self, (dx, dy)):
		hadj, vadj = self._gtk_adjustments()
		hadj.step_increment = float(dx) # Amazingly, ints are not
		vadj.step_increment = float(dy) # acceptable here.
	
	#
	#		Internal
	#

	def _gtk_adjustments(self):
		gtk_widget = self._gtk_inner_widget
		hadj = gtk_widget.get_hadjustment()
		vadj = gtk_widget.get_vadjustment()
		return hadj, vadj

export(ScrollableView)
