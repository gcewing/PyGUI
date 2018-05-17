#
#		Python GUI - DrawableViews - Gtk
#

import os, traceback
from math import floor, ceil
from gi.repository import Gtk, Gdk, cairo
from GUI.Canvases import Canvas
from GUI.Events import Event
from GUI.GDrawableContainers import DrawableContainer as GDrawableContainer

class DrawableContainer(GDrawableContainer):

	#_extent_origin = (0, 0)

	def __init__(self, _gtk_outer = None, **kwds):
		gtk_layout = Gtk.Layout()
		gtk_layout.add_events(Gdk.EventMask.EXPOSURE_MASK)
		gtk_layout.show()
		self._gtk_connect(gtk_layout, 'draw', self._gtk_draw_signal)
		if _gtk_outer:
			_gtk_outer.add(gtk_layout)
		else:
			_gtk_outer = gtk_layout
		GDrawableContainer.__init__(self,
			_gtk_outer = _gtk_outer, _gtk_inner = gtk_layout,
			_gtk_focus = gtk_layout, _gtk_input = gtk_layout)
		self.set(**kwds)
	
	#
	#		Other methods
	#

	def with_canvas(self, proc):
		hadj, vadj = self._gtk_adjustments()
		clip = rect_sized((hadj.value, vadj.value), self.size)
#		canvas = Canvas._from_gdk_drawable(self._gtk_inner_widget.bin_window)
		context = Gdk.cairo_create(self._gtk_inner_widget.get_bin_window())
		self._gtk_prepare_cairo_context(context)
		canvas = Canvas._from_cairo_context(context)
		proc(canvas)
	
	def invalidate_rect(self, (l, t, r, b)):
		x = int(floor(l))
		y = int(floor(t))
		w = int(ceil(r - l))
		h = int(ceil(b - t))
		self._gtk_inner_widget.queue_draw_area(x, y, w, h)
	
	def update(self):
		gdk_window = self._gtk_inner_widget.bin_window
		gdk_window.process_updates()

	#
	#		Internal
	#

	def _gtk_draw_signal(self, context):
		try:
			self._gtk_prepare_cairo_context(context)
			clip = context.clip_extents()
			canvas = Canvas._from_cairo_context(context)
			self.draw(canvas, clip)
		except:
			print "------------------ Exception while drawing ------------------"
			traceback.print_exc()

	def _gtk_prepare_cairo_context(self, context):
		pass
