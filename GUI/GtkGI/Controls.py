#
#   Python GUI - Controls - Gtk
#

from gi.repository import Gtk
from GUI.Enumerations import EnumMap
from GUI.Colors import Color
from GUI.Fonts import Font
from GUI.GControls import Control as GControl

_justs = ['left', 'center', 'right']

_just_to_gtk_alignment = EnumMap("justification",
	left = (0.0, Gtk.Justification.LEFT),
	centre = (0.5, Gtk.Justification.CENTER),
	center = (0.5, Gtk.Justification.CENTER),
	right = (1.0, Gtk.Justification.RIGHT),
)
	
class Control(GControl):
	#  A component which encapsulates a Gtk control widget.
	
	_font = None
	_color = None
	
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
		return self._color
#		gdk_color = self._gtk_title_widget.get_style().fg[Gtk.StateType.NORMAL]
#		return Color._from_gdk_color(gdk_color)
	
	def set_color(self, v):
		#self._gtk_title_widget.modify_fg(Gtk.StateType.NORMAL, v._gdk_color)
		self._color = v
		self._gtk_title_widget.override_color(Gtk.StateType.NORMAL, v._gdk_rgba)
			
	def get_font(self):
		font = self._font
		if not font:
			font = Font._from_pango_description(self._gtk_title_widget.style.font_desc)
		return font
		
	def set_font(self, f):
		self._font = f
		gtk_title = self._gtk_title_widget
#		print "Control.set_font: gtk_title =", gtk_title ###
#		pd = f._pango_description ###
#		print "...family =", pd.get_family() ###
#		print "...size =", pd.get_size() ###
		#gtk_title.modify_font(f._pango_description)
		gtk_title.override_font(f._pango_description)
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
