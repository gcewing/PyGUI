#
#		Python GUI - Fonts - Generic
#

import sys
from GUI.Properties import overridable_property

class Font(object):
	"""A Font object represents a set of characters of a particular 
	typeface, style and size. Font objects are immutable.
	
	Constructors:
		Font(family, size, style)
			family = family name
			size	 = size in points
			style	 = a list of 'bold', 'italic'
	
	Properties:
		family	-->	 string
		size		-->	 number
		style		-->	 ['bold', 'italic']
		ascent	-->	 number
		descent -->	 number
		leading	-->	 number
		height	-->	 number
		cap_height	-->	 number
		x_height	  -->	 number
		line_height	-->	 number
	"""
	
	family = overridable_property('family', "Family name ('Times', 'Helvetica', etc.)")
	size = overridable_property('size', "Size in points")
	style = overridable_property('style', "A list of 'bold', 'italic'")
	ascent = overridable_property('ascent', "Distance from baseline to top of highest character")
	descent = overridable_property('descent', "Distance from baseline to bottom of lowest character")
	height = overridable_property('height', "Sum of ascent and descent")
	cap_height = overridable_property('cap_height', "Height above baseline of capital letters")
	x_height = overridable_property('x_height', "Height above baseline of lowercase letters without ascenders")
	leading = overridable_property('leading', "Recommended extra space between lines")
	line_height = overridable_property('line_height', "Recommended distance between baselines")
	
	def get_cap_height(self):
		#  Approximation for platforms not supporting this
		return self.ascent
	
	def get_x_height(self):
		#  Approximation for platforms not supporting this
		return self.ascent - self.descent
	
	def get_leading(self):
		return self.line_height - self.height
	
	def but(self, family = None, size = None, style = None,
			style_includes = None, style_excludes = None):
		"""Return a new Font that is the same as this one except for the
		specified characteristics."""
		if not family:
			family = self.family
		if not size:
			size = self.size
		if style is None:
			style = self.style
		style = style[:]
		if style_includes:
			for item in style_includes:
				style.append(item)
		if style_excludes:
			for item in style_excludes:
				if item in style:
					style.remove(item)
		return self.__class__(family, size, style)
	
	def width(self, s, start = 0, end = None):
		"""width(s [,start [,end ]])
		The width of the specified part of the given string in this font."""
		if start or end is not None:
			if end is None:
				end = len(s)
			s = s[start:end]
		return self._width(s)
	
	def _width(self, s):
		raise NotImplementedError

	def x_to_pos(self, s, x):
		"""Given a number of pixels measured from the left of
		the given string, returns the nearest inter-character position. 
		Returns 0 if x is negative, and len(string) if x is beyond the 
		right end of the string."""
		raise NotImplementedError

	def __str__(self):
		return "Font(%r,%g,%s)" % (self.family, self.size, self.style)
