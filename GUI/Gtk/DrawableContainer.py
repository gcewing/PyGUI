#
#		Python GUI - DrawableViews - Gtk
#

import os, traceback
from math import floor, ceil
import gtk
from gtk import gdk
from GUI import export
from GUI import Canvas, Event, rgb
from GUI.StdColors import grey
from GUI.GDrawableContainers import DrawableContainer as GDrawableContainer

class DrawableContainer(GDrawableContainer):

	_background_color = grey

	def __init__(self, _gtk_outer = None, **kwds):
		gtk_layout = gtk.Layout()
		gtk_layout.add_events(gdk.EXPOSURE_MASK)
		gtk_layout.show()
		self._gtk_connect(gtk_layout, 'expose-event',
			self._gtk_expose_event_signal)
		if _gtk_outer:
			_gtk_outer.add(gtk_layout)
		else:
			_gtk_outer = gtk_layout
		GDrawableContainer.__init__(self, _gtk_outer = _gtk_outer, _gtk_inner = gtk_layout,
			_gtk_focus = gtk_layout, _gtk_input = gtk_layout)
		self.set(**kwds)
	
	#
	#		Other methods
	#

	def with_canvas(self, proc):
		hadj, vadj = self._gtk_adjustments()
		clip = rect_sized((hadj.value, vadj.value), self.size)
		canvas = Canvas._from_gdk_drawable(self._gtk_inner_widget.bin_window)
		proc(canvas)
	
	def invalidate_rect(self, (l, t, r, b)):
		gdk_window = self._gtk_inner_widget.bin_window
		if gdk_window:
			gdk_rect = (int(floor(l)), int(floor(t)),
				int(ceil(r - l)), int(ceil(b - t)))
			#print "View.invalidate_rect: gdk_rect =", gdk_rect ###
			gdk_window.invalidate_rect(gdk_rect, 0)
	
	def update(self):
		gdk_window = self._gtk_inner_widget.bin_window
		gdk_window.process_updates()

	#
	#		Internal
	#

	def _gtk_expose_event_signal(self, gtk_event):
		try:
			#print "View._gtk_expose_event_signal:", self ###
			l, t, w, h = gtk_event.area
			clip = (l, t, l + w, t + h)
			#print "...clip =", clip ###
			gtk_layout = self._gtk_inner_widget
			canvas = Canvas._from_gdk_drawable(gtk_layout.bin_window)
			update = self._draw_background(canvas, clip)
			self.draw(canvas, update)
		except:
			print "------------------ Exception while drawing ------------------"
			traceback.print_exc()

export(DrawableContainer)
