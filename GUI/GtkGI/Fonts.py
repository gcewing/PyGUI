#
#		Python GUI - Fonts - Gtk
#

import sys
from gi.repository import Pango
from gi.repository import Gtk
from gi.repository import Gdk
from GUI.GFonts import Font as GFont

class Font(GFont):

	#_gdk_font = None
	_pango_font = None
	_pango_metrics = None
	_pango_layout = None

#	def _from_gdk_font(cls, gdk_font):
#		font = cls.__new__(cls)
#		font._gdk_font = gdk_font
#		return font
#	
#	_from_gdk_font = classmethod(_from_gdk_font)
	
	def _from_pango_description(cls, pango_description):
		font = cls.__new__(cls)
		font._pango_description = pango_description
		return font
	
	_from_pango_description = classmethod(_from_pango_description)

	def __init__(self, family, size = 12, style = []):
		if 'italic' in style:
			pango_style = Pango.Style.ITALIC
		else:
			pango_style = Pango.Style.NORMAL
		if 'bold' in style:
			pango_weight = Pango.Weight.BOLD
		else:
			pango_weight = Pango.Weight.NORMAL
		pfd = Pango.FontDescription()
		pfd.set_family(family)
		pfd.set_size(int(round(size * Pango.SCALE)))
		pfd.set_style(pango_style)
		pfd.set_weight(pango_weight)
		self._pango_description = pfd
	
	def get_family(self):
		return self._pango_description.get_family()
	
	def get_size(self):
		return self._pango_description.get_size() / Pango.SCALE
	
	def get_style(self):
		style = []
		pfd = self._pango_description
		if pfd.get_weight() > Pango.Weight.NORMAL:
			style.append('bold')
		if pfd.get_style() <> Pango.Style.NORMAL:
			style.append('italic')
		return style
	
	def get_ascent(self):
		self._get_pango_metrics()
		result = self._ascent
		return result
	
	def get_descent(self):
		self._get_pango_metrics()
		return self._descent
	
	def get_height(self):
		self._get_pango_metrics()
		return self._ascent + self._descent
	
	def get_line_height(self):
		return self.get_height()
	
	def _get_pango_metrics(self):
		#print "Font._get_pango_metrics: enter" ###
		pfm = self._pango_metrics
		if not pfm:
			pf = self._get_pango_font()
			pfm = pf.get_metrics(None)
			self._pango_metrics = pfm
			self._ascent = pfm.get_ascent() / Pango.SCALE
			self._descent = pfm.get_descent() / Pango.SCALE
		return pfm
	
	def _get_pango_font(self):
		pf = self._pango_font
		if not pf:
			pf = _pango_context.load_font(self._pango_description)
			if not pf:
				raise ValueError("Unable to load Pango font for %s" % self)
			self._pango_font = pf
		return pf
	
	def width(self, s, start = 0, end = sys.maxint):
		layout = self._get_pango_layout(s[start:end], True)
		return layout.get_pixel_size()[0]

	def text_size(self, text):
		layout = self._get_pango_layout(text, False)
		return layout.get_pixel_size()

	def x_to_pos(self, s, x):
		layout = self._get_pango_layout(s, True)
		return pango_layout.xy_to_index(x, 0)
	
	def _get_pango_layout(self, text, single_paragraph_mode):
		layout = self._pango_layout
		if not layout:
			layout = Pango.Layout(_pango_context)
			layout.set_font_description(self._pango_description)
			self._pango_layout = layout
		layout.set_single_paragraph_mode(single_paragraph_mode)
		layout.set_text(text, len(text))
		return layout


_pango_context = Gtk.Label().create_pango_context()
