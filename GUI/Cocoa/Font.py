#
#   Python GUI - Fonts - PyObjC
#

import sys
from AppKit import NSFont, NSFontManager, NSBoldFontMask, NSItalicFontMask, \
	NSLayoutManager
from GUI import export
from GUI.GFonts import Font as GFont

_ns_font_manager = NSFontManager.sharedFontManager()
_ns_layout_manager = NSLayoutManager.alloc().init()

class Font(GFont):
	#  _ns_font   NSFont
	
	def _from_ns_font(cls, ns_font):
		font = cls.__new__(cls)
		font._ns_font = ns_font
		return font
	
	_from_ns_font = classmethod(_from_ns_font)
	
	def __init__(self, family, size = 12, style = []):
		traits = 0
		if 'bold' in style:
			traits |= NSBoldFontMask
		if 'italic' in style:
			traits |= NSItalicFontMask
		self._ns_font = _ns_font_manager.fontWithFamily_traits_weight_size_(
			family, traits, 5, size)
		if not self._ns_font:
			import StdFonts
			self._ns_font = StdFonts.application_font._ns_font
	
	def get_family(self):
		return self._ns_font.familyName()
	
	def get_size(self):
		return self._ns_font.pointSize()
	
	def get_style(self):
		style = []
		traits = _ns_font_manager.traitsOfFont_(self._ns_font)
		if traits & NSBoldFontMask:
			style.append('bold')
		if traits & NSItalicFontMask:
			style.append('italic')
		return style
	
	def get_ascent(self):
		return self._ns_font.ascender()
	
	def get_descent(self):
		return -self._ns_font.descender()
	
	def get_height(self):
		ns_font = self._ns_font
		a = ns_font.ascender()
		d = ns_font.descender()
		return a - d
	
	def get_cap_height(self):
		return self._ns_font.capHeight()
	
	def get_x_height(self):
		return self._ns_font.xHeight()
	
	def get_line_height(self):
		# Adding 1 here to match what NSTextField seems to do
		return _ns_layout_manager.defaultLineHeightForFont_(self._ns_font) + 1
	
	def width(self, s, start = 0, end = sys.maxint):
		return self._ns_font.widthOfString_(s[start:end])

export(Font)

