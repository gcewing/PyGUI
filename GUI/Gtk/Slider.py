#
#   Python GUI - Slider - Gtk
#

import gtk
from GUI import export
from GUI.GSliders import Slider as GSlider

class Slider(GSlider):

	_gtk_tick_length = 8
	_gtk_tick_inset = 18

	def __init__(self, orient = 'h', ticks = 0, **kwds):
		self._orient = orient
		self._ticks = ticks
		self._discrete = False
		self._live = True
		self._gtk_ticks = None
		length = 100
		gtk_adjustment = gtk.Adjustment(upper = 1.0)
		xs = 0.0
		ys = 0.0
		if orient == 'h':
			gtk_scale = gtk.HScale(gtk_adjustment)
			gtk_scale.set_size_request(length, -1)
			gtk_box = gtk.VBox()
			xs = 1.0
		elif orient == 'v':
			gtk_scale = gtk.VScale(gtk_adjustment)
			gtk_scale.set_size_request(-1, length)
			gtk_box = gtk.HBox()
			ys = 1.0
		else:
			raise ValueError("Invalid orientation, should be 'h' or 'v'")
		gtk_scale.set_draw_value(False)
		self._gtk_scale = gtk_scale
		gtk_box.pack_start(gtk_scale)
		self._gtk_box = gtk_box
		if ticks:
			self._gtk_create_ticks()
		gtk_alignment = gtk.Alignment(xalign = 0.5, yalign = 0.5,
			xscale = xs, yscale = ys)
		gtk_alignment.add(gtk_box)
		gtk_alignment.show_all()
		self._gtk_connect(gtk_adjustment, 'value-changed', self._gtk_value_changed)
		self._gtk_connect(gtk_scale, 'change-value', self._gtk_change_value)
		self._gtk_connect(gtk_scale, 'button-release-event', self._gtk_button_release)
		self._gtk_scale = gtk_scale
		self._gtk_adjustment = gtk_adjustment
		self._gtk_enable_action = True
		GSlider.__init__(self, _gtk_outer = gtk_alignment, **kwds)
		
	def get_min_value(self):
		return self._min_value

	def set_min_value(self, x):
		self._gtk_adjustment.lower = x

	def get_max_value(self):
		return self._max_value

	def set_max_value(self, x):
		self._gtk_adjustment.upper = x

	def get_value(self):
		return self._gtk_adjustment.value
	
	def set_value(self, x):
		self._gtk_enable_action = False
		self._gtk_adjustment.value = x
		self._gtk_enable_action = True
	
	def get_ticks(self):
		return self._ticks
	
	def set_ticks(self, x):
		self._ticks = x
		if x:
			self._gtk_create_ticks()
		else:
			self._gtk_destroy_ticks()
	
	def get_discrete(self):
		return self._discrete
	
	def set_discrete(self, x):
		self._discrete = x

	def get_live(self):
		return self._live

	def set_live(self, x):
		self._live = x
	
	def _gtk_create_ticks(self):
		if not self._gtk_ticks:
			gtk_ticks = gtk.DrawingArea()
			length = self._gtk_tick_length
			if self._orient == 'h':
				gtk_ticks.set_size_request(-1, length)
			else:
				gtk_ticks.set_size_request(length, -1)
			self._gtk_ticks = gtk_ticks
			self._gtk_connect(gtk_ticks, 'expose-event', self._gtk_draw_ticks)
			self._gtk_box.pack_start(gtk_ticks)
	
	def _gtk_destroy_ticks(self):
		gtk_ticks = self._gtk_ticks
		if gtk_ticks:
			gtk_ticks.destroy()
			self._gtk_ticks = None
	
	def _gtk_draw_ticks(self, event):
		gtk_ticks = self._gtk_ticks
		gdk_win = gtk_ticks.window
		gtk_style = gtk_ticks.style
		orient = self._orient
		steps = self._ticks - 1
		_, _, w, h = gtk_ticks.allocation
		u0 = self._gtk_tick_inset
		v0 = 0
		if orient == 'h':
			draw_line = gtk_style.paint_vline
			u1 = w - u0
			v1 = h
		else:
			draw_line = gtk_style.paint_hline
			u1 = h - u0
			v1 = w
		state = gtk.STATE_NORMAL
		for i in xrange(steps + 1):
			u = u0 + i * (u1 - u0) / steps
			draw_line(gdk_win, state, None, gtk_ticks, "", v0, v1, u)
	
	def _gtk_value_changed(self):
		if self._live and self._gtk_enable_action:
			self.do_action()

	def _gtk_change_value(self, event_type, value):
		gtk_adjustment = self._gtk_adjustment
		vmin = gtk_adjustment.lower
		vmax = gtk_adjustment.upper
		value = min(max(vmin, value), vmax)
		if self._discrete:
			steps = self._ticks - 1
			if steps > 0:
				q = round(steps * (value - vmin) / (vmax - vmin))
				value = vmin + q * (vmax - vmin) / steps
		if gtk_adjustment.value <> value:
			gtk_adjustment.value = value
		return True

	def _gtk_button_release(self, gtk_event):
		self.do_action()

export(Slider)
