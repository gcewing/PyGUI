#
#   Python GUI - Controls - Gtk
#

import gtk
from GUI import export
from GUI.Enumerations import EnumMap
from GUI import Color
from GUI import Font
from GUI.GControls import Control as GControl

_justs = ['left', 'center', 'right']

_just_to_gtk_alignment = EnumMap("justification",
	left = (0.0, gtk.JUSTIFY_LEFT),
	centre = (0.5, gtk.JUSTIFY_CENTER),
	center = (0.5, gtk.JUSTIFY_CENTER),
	right = (1.0, gtk.JUSTIFY_RIGHT),
)
	
class Control(GControl):
	#  A component which encapsulates a Gtk control widget.
	
	_font = None
	
	def __init__(self, _gtk_outer = None, _gtk_title = None, **kwds):
		self._gtk_title_widget = _gtk_title or _gtk_outer
		GControl.__init__(self, _gtk_outer = _gtk_outer,
			_gtk_focus = kwds.pop('_gtk_focus', _gtk_outer),
			**kwds)
	
	def get_title(self):
		return self._gtk_title_widget.get_label()
	
	def set_title(self, v):
		self._gtk_title_widget.set_label(v)
	
	def get_enabled(self):
		#return self._gtk_outer_widget.get_sensitive()
		return self._gtk_outer_widget.get_property('sensitive')
	
	def set_enabled(self, v):
		self._gtk_outer_widget.set_sensitive(v)
	
	def get_color(self):
		gdk_color = self._gtk_title_widget.style.fg[gtk.STATE_NORMAL]
		return Color._from_gdk_color(gdk_color)
	
	def set_color(self, v):
		self._gtk_title_widget.modify_fg(gtk.STATE_NORMAL, v._gdk_color)
			
	def get_font(self):
		font = self._font
		if not font:
			font = Font._from_pango_description(self._gtk_title_widget.style.font_desc)
		return font
		
	def set_font(self, f):
		self._font = f
		gtk_title = self._gtk_title_widget
		gtk_title.modify_font(f._pango_description)
		gtk_title.queue_resize()
		
	def get_just(self):
		h = self._gtk_get_alignment()
		return _justs[int(round(2.0 * h))]
	
	def set_just(self, v):
		fraction, just = _just_to_gtk_alignment[v]
		self._gtk_set_alignment(fraction, just)
	
	def set_lines(self, num_lines):
		line_height = self.font.text_size("X")[1]
		#print "Control.set_lines: line_height =", line_height ###
		self.height = num_lines * line_height + self._vertical_padding

	def _gtk_get_alignment(self):
		raise NotImplementedError

	def _gtk_set_alignment(self, h):
		raise NotImplementedError

export(Control)
