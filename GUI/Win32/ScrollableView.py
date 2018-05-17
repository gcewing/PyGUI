#--------------------------------------------------------------------
#
#   PyGUI - ScrollableView - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui
from GUI import export
from GUI.WinUtils import win_plain_class, win_none
from GUI import Canvas
from GUI.GScrollableViews import ScrollableView as GScrollableView, \
	default_extent, default_line_scroll_amount, default_scrolling
from GUI.Geometry import add_pt, sub_pt, offset_rect, offset_rect_neg
from GUI.GDrawableContainers import default_size
from GUI.Geometry import offset_rect_neg

win_style = wc.WS_CHILD | wc.WS_CLIPCHILDREN | wc.WS_CLIPSIBLINGS | \
	wc.WS_VISIBLE  ###| wc.WS_VSCROLL| wc.WS_HSCROLL
win_ex_style = 0 # wc.WS_EX_CLIENTEDGE
win_default_rect = (0, 0, default_size[0], default_size[1])
win_scroll_flags = wc.SW_INVALIDATE | wc.SW_SCROLLCHILDREN
win_swp_flags = wc.SWP_DRAWFRAME #| wc.SWP_FRAMECHANGED

class ScrollableView(GScrollableView):

	_line_scroll_amount = default_line_scroll_amount
	_extent = (500, 500)

	def __init__(self, **kwds):
		kwds.setdefault('border', True)
		kwds.setdefault('extent', default_extent)
		kwds.setdefault('scrolling', default_scrolling)
		win = ui.CreateWnd()
		win.CreateWindowEx(win_ex_style, win_plain_class, None, win_style, win_default_rect, win_none, 0)
		win.HookMessage(self._win_wm_hscroll, wc.WM_HSCROLL)
		win.HookMessage(self._win_wm_vscroll, wc.WM_VSCROLL)
		GScrollableView.__init__(self, _win = win)
		self.set(**kwds)

	def get_hscrolling(self):
		return self._win_get_flag(wc.WS_HSCROLL)
	
	def get_vscrolling(self):
		return self._win_get_flag(wc.WS_VSCROLL)
	
	def set_hscrolling(self, x):
		#print "ScrollableView.set_hscrolling:", x ###
		self._win_set_flag(x, wc.WS_HSCROLL, win_swp_flags)
		self._win_update_h_scrollbar()
	
	def set_vscrolling(self, x):
		#print "ScrollableView.set_vscrolling:", x ###
		self._win_set_flag(x, wc.WS_VSCROLL, win_swp_flags)
		self._win_update_v_scrollbar()
	
	def set_border(self, x):
		self._border = x
		self._win_set_ex_flag(x, wc.WS_EX_CLIENTEDGE, win_swp_flags)
	
	def get_line_scroll_amount(self):
		return self._line_scroll_amount
	
	def get_extent(self):
		return self._extent
	
	def set_extent(self, extent):
		self._extent = extent
		self._win_update_scroll_sizes()
	
	def get_scroll_offset(self):
		return self._h_scroll_offset, self._v_scroll_offset
	
	def set_scroll_offset(self, p):
		px = int(round(p[0]))
		py = int(round(p[1]))
		if px <> self._h_scroll_offset or py <> self._v_scroll_offset:
			self._win_update_scroll_offset(px, py)
	
	def _win_update_scroll_sizes(self):
		self._win_update_scroll_offset(self._h_scroll_offset, self._v_scroll_offset)

	def _win_update_scroll_offset(self, px, py):
		ex, ey = self.extent
		vx, vy = self.content_size
		xmax = max(0, ex - vx)
		ymax = max(0, ey - vy)
		x = max(0, min(px, xmax))
		y = max(0, min(py, ymax))
		self._win_scroll_to(x, y)
		self._win_update_h_scrollbar()
		self._win_update_v_scrollbar()
	
	def _win_update_h_scrollbar(self):
		self._win_update_scrollbar(self.hscrolling, wc.SB_HORZ, 0)
	
	def _win_update_v_scrollbar(self):
		self._win_update_scrollbar(self.vscrolling, wc.SB_VERT, 1)
	
	def _win_update_scrollbar(self, enabled, nbar, i):
		#  It is important not to update a disabled scrollbar, or
		#  subtle problems occur.
		if enabled:
			#print "ScrollableView._win_update_scrollbar:", enabled, nbar, i ###
			f = wc.SIF_DISABLENOSCROLL
			info = (f, 0, self.extent[i], self.content_size[i], self.scroll_offset[i])
			self._win.SetScrollInfo(nbar, info, True)

	def _scroll_range(self):
		return (xmax, ymax)
	
	def _win_scroll_to(self, x, y):
		dx = self._h_scroll_offset - x
		dy = self._v_scroll_offset - y
		if dx or dy:
			hwnd = self._win.GetSafeHwnd()
			gui.ScrollWindowEx(hwnd, dx, dy, None, None, None, win_scroll_flags)
			self._h_scroll_offset = x
			self._v_scroll_offset = y
	
	def set_bounds(self, bounds):
		GScrollableView.set_bounds(self, bounds)
		self._win_update_scroll_sizes()
	
	def _invalidate_rect(self, r):
		win = self._win
		s = self.scroll_offset
		self._win.InvalidateRect(offset_rect_neg(r, s))

	def local_to_global(self, p):
		q = sub_pt(p, self.scroll_offset)
		return self._win.ClientToScreen(q)
	
	def global_to_local(self, g):
		q = self._win.ScreenToClient(g)
		return add_pt(q, self.scroll_offset)

#	def _win_prepare_dc(self, dc):
#		dc.SetWindowOrg(self.scroll_offset)
	
	def _win_scroll_offset(self):
		return self.scroll_offset

	def _win_wm_hscroll(self, message):
		code = message[2] & 0xffff
		if code == 0:
			self.scroll_line_left()
		elif code == 1:
			self.scroll_line_right()
		elif code == 2:
			self.scroll_page_left()
		elif code == 3:
			self.scroll_page_right()
		elif code == 5:
			x = self._win_thumb_track_pos(wc.SB_HORZ)
			self.scroll_offset = (x, self._v_scroll_offset)
	
	def _win_wm_vscroll(self, message):
		code = message[2] & 0xffff
		if code == 0:
			self.scroll_line_up()
		elif code == 1:
			self.scroll_line_down()
		elif code == 2:
			self.scroll_page_up()
		elif code == 3:
			self.scroll_page_down()
		elif code == 5:
			y = self._win_thumb_track_pos(wc.SB_VERT)
			self.scroll_offset = (self._h_scroll_offset, y)

	def _win_thumb_track_pos(self, nbar):
		info = self._win.GetScrollInfo(nbar)
		return info[5]

	def _win_adjust_bounds(self, bounds):
		return offset_rect_neg(bounds, self.scroll_offset)

export(ScrollableView)
