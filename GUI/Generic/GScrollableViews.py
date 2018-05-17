#-------------------------------------------------------------------------------
#
#		Python GUI - Scrollable Views - Generic
#
#-------------------------------------------------------------------------------

from GUI.Geometry import rect_sized, add_pt, sub_pt
from GUI.Properties import overridable_property
from GUI.Geometry import sect_rect
from GUI import DrawableContainer, ScrollableBase

default_extent = (300, 300)
default_line_scroll_amount = (16, 16)
default_scrolling = 'hv'

class ScrollableView(DrawableContainer, ScrollableBase):
	"""A ScrollableView is a 2D drawing area having its own coordinate
	system and clipping area, with support for scrolling."""

#	scrolling = overridable_property('scrolling',
#		"String containing 'h' for horizontal and 'v' for vertical scrolling.")
#	
#	hscrolling = overridable_property('hscrolling',
#		"True if horizontal scrolling is enabled.")
#	
#	vscrolling = overridable_property('vscrolling',
#		"True if vertical scrolling is enabled.")
	
	extent = overridable_property('extent',
		"Size of scrollable area in local coordinates.")

	scroll_offset = overridable_property('scroll_offset',
		"Current scrolling position.")

	line_scroll_amount = overridable_property('line_scroll_amount',
		"Tuple specifying horizontal and vertical line scrolling increments.")
	
	background_color = overridable_property('background_color',
		"Color with which to fill areas outside the extent, or None")

	#scroll_bars = overridable_property('scroll_bars',
	#	"Attached ScrollBar instances.")
	#
	##  _scroll_bars          [ScrollBar]
	
	def set(self, **kwds):
		if 'scrolling' in kwds:
			self.scrolling = kwds.pop('scrolling')
		DrawableContainer.set(self, **kwds)

#	def get_scrolling(self):
#		chars = []
#		if self.hscrolling:
#			chars.append('h')
#		if self.vscrolling:
#			chars.append('v')
#		return ''.join(chars)
#	
#	def set_scrolling(self, value):
#		self.hscrolling = 'h' in value
#		self.vscrolling = 'v' in value

	def viewed_rect(self):
		"""Return the rectangle in local coordinates bounding the currently
		visible part of the extent."""
		return rect_sized(self.scroll_offset, self.size)

	def get_print_extent(self):
		return self.extent
	
	def get_background_color(self):
		return self._background_color
	
	def set_background_color(self, x):
		self._background_color = x
		self.invalidate()

	#
	#		Coordinate transformation
	#

	def local_to_container_offset(self):
		return sub_pt(self.position, self.scroll_offset)

	#
	#		Scrolling
	#

	def h_line_scroll_amount(self):
		"""Return the horizontal line scroll increment."""
		return self.line_scroll_amount[0]

	def v_line_scroll_amount(self):
		"""Return the vertical line scroll increment."""
		return self.line_scroll_amount[1]

	def h_page_scroll_amount(self):
		"""Return the horizontal page scroll increment."""
		return self.width - self.h_line_scroll_amount()

	def v_page_scroll_amount(self):
		"""Return the vertical page scroll increment."""
		return self.height - self.v_line_scroll_amount()

	def scroll_by(self, dx, dy):
		"""Scroll by the given amount horizontally and vertically."""
		self.scroll_offset = add_pt(self.scroll_offset, (dx, dy))

	def scroll_line_left(self):
		"""Called by horizontal scroll bar to scroll left by one line."""
		self.scroll_by(-self.h_line_scroll_amount(), 0)

	def scroll_line_right(self):
		"""Called by horizontal scroll bar to scroll right by one line."""
		self.scroll_by(self.h_line_scroll_amount(), 0)

	def scroll_line_up(self):
		"""Called by vertical scroll bar to scroll up by one line."""
		self.scroll_by(0, -self.v_line_scroll_amount())

	def scroll_line_down(self):
		"""Called by vertical scroll bar to scroll down by one line."""
		self.scroll_by(0, self.v_line_scroll_amount())

	def scroll_page_left(self):
		"""Called by horizontal scroll bar to scroll left by one page."""
		self.scroll_by(-self.h_page_scroll_amount(), 0)

	def scroll_page_right(self):
		"""Called by horizontal scroll bar to scroll right by one page."""
		self.scroll_by(self.h_page_scroll_amount(), 0)

	def scroll_page_up(self):
		"""Called by vertical scroll bar to scroll up by one page."""
		self.scroll_by(0, -self.v_page_scroll_amount())

	def scroll_page_down(self):
		"""Called by vertical scroll bar to scroll down by one page."""
		self.scroll_by(0, self.v_page_scroll_amount())

	#
	#   Background drawing
	#
	
	def _draw_background(self, canvas, clip_rect):
		#  If the view has a background color, uses it to fill the parts of the
		#  clip_rect that are outside the view's extent and returns the remaining
		#  rectangle. Otherwise, returns the clip_rect unchanged.
		color = self._background_color
		if color:
			vl, vt, vr, vb = clip_rect
			ew, eh = self.extent
			if vr > ew or vb > eh:
				#if getattr(self, "_debug_bg", False): ###
				#	print "ScrollableView: old backcolor =", canvas.backcolor ###
				canvas.gsave()
				canvas.backcolor = color
				if ew < vr:
					#if getattr(self, "_debug_bg", False): ###
					#	print "ScrollableView: erasing", (ew, vt, vr, vb) ###
					canvas.erase_rect((ew, vt, vr, vb))
				if eh < vb:
					if getattr(self, "_debug_bg", False): ###
						print "ScrollableView: erasing", (vl, eh, ew, vb) ###
					canvas.erase_rect((vl, eh, ew, vb))
				canvas.grestore()
				#if getattr(self, "_debug_bg", False): ###
				#	print "ScrollableView: restored backcolor =", canvas.backcolor ###
				return sect_rect(clip_rect, (0, 0, ew, eh))
		return clip_rect
