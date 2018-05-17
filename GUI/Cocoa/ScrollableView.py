#
#		Python GUI - Scrollable Views - PyObjC
#

from Foundation import NSPoint, NSMakeRect
from AppKit import NSScrollView
from GUI import export
from GUI.GScrollableViews import ScrollableView as GScrollableView, \
	default_extent, default_line_scroll_amount, default_scrolling
from GUI.Geometry import ns_rect_to_rect

class ScrollableView(GScrollableView):

	_ns_scrollable = True

	def __init__(self, extent = default_extent,
			line_scroll_amount = default_line_scroll_amount,
			scrolling = default_scrolling,
			**kwds):
		GScrollableView.__init__(self,
			extent = extent, line_scroll_amount = line_scroll_amount,
			scrolling = scrolling, **kwds)
	
#	def get_hscrolling(self):
#		return self._ns_view.hasHorizontalScroller()
#	
#	def set_hscrolling(self, value):
#		self._ns_view.setHasHorizontalScroller_(value)
#	
#	def get_vscrolling(self):
#		return self._ns_view.hasVerticalScroller()
#	
#	def set_vscrolling(self, value):
#		self._ns_view.setHasVerticalScroller_(value)
	
#	def get_extent(self):
#		(l, t), (w, h) = self._ns_inner_view.bounds()
#		return (l, t, l + w, t + h)
	
	def get_extent(self):
		return self._ns_inner_view.bounds().size

#	def set_extent(self, (l, t, r, b)):
#		w = r - l
#		h = b - t
#		ns_docview = self._ns_inner_view
#		ns_docview.setFrame_(NSMakeRect(0, 0, w, h))
#		ns_docview.setBounds_(NSMakeRect(l, t, w, h))
#		self.invalidate()
	
	def set_extent(self, (w, h)):
		r = NSMakeRect(0, 0, w, h)
		ns_docview = self._ns_inner_view
		ns_docview.setFrame_(r)
		ns_docview.setBounds_(r)
		self.invalidate()
	
	def get_content_size(self):
		return self._ns_view.contentSize()
	
	def set_content_size(self, size):
		ns = self._ns_view
		self.size = NSScrollView.\
			frameSizeForContentSize_hasHorizontalScroller_hasVerticalScroller_borderType_(
			size, ns.hasHorizontalScroller(), ns.hasVerticalScroller(), ns.borderType())

	def get_scroll_offset(self):
		ns_clip_view = self._ns_view.contentView()
		x, y = ns_clip_view.bounds().origin
		return x, y
	
	def set_scroll_offset(self, (x, y)):
		ns_view = self._ns_view
		ns_clip_view = ns_view.contentView()
		new_pt = ns_clip_view.constrainScrollPoint_(NSPoint(x, y))
		ns_clip_view.scrollToPoint_(new_pt)
		ns_view.reflectScrolledClipView_(ns_clip_view)

	def get_line_scroll_amount(self):
		ns_view = self._ns_view
		x = ns_view.horizontalLineScroll()
		y = ns_view.verticalLineScroll()
		return x, y
	
	def set_line_scroll_amount(self, (x, y)):
		ns_view = self._ns_view
		ns_view.setHorizontalLineScroll_(x)
		ns_view.setVerticalLineScroll_(y)
		ns_view.setHorizontalPageScroll_(x)
		ns_view.setVerticalPageScroll_(y)

	def viewed_rect(self):
		ns_rect = self._ns_view.contentView().documentVisibleRect()
		return ns_rect_to_rect(ns_rect)

export(ScrollableView)
