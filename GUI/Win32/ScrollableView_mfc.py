#--------------------------------------------------------------------
#
#   PyGUI - ScrollableView - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI.Components import win_none
from GUI.Canvases import Canvas
from GUI.GScrollableViews import ScrollableView as GScrollableView, \
	default_extent, default_line_scroll_amount
from GUI.Geometry import add_pt, sub_pt, offset_rect, offset_rect_neg

win_style = ui.AFX_WS_DEFAULT_VIEW

#print "ScrollableViews: Creating dummy doc"
#  PyWin32 insists on being given a CDocument when creating a CScrollView,
#  and doesn't provide any way of creating a real one without using a resource.

if 1:
	#  The following uses a resource included in win32ui.pyd.
	import pywin.mfc.object
	win_dummy_doc_template = pywin.mfc.object.CmdTarget(
		ui.CreateDocTemplate(ui.IDR_PYTHONTYPE))
	ui.GetApp().AddDocTemplate(win_dummy_doc_template)
	def win_get_dummy_doc():
		return win_dummy_doc_template.DoCreateDoc()
else:
	#  The following hack creates something that looks enough
	#  like a CDocument to keep it happy. But it doesn't work with
	#  pywin32 builds later than 212.
	win_dummy_doc = ui.CreateRichEditView().GetDocument()
	def win_get_dummy_doc():
		return win_dummy_doc

class ScrollableView(GScrollableView):

	_line_scroll_amount = default_line_scroll_amount

	def __init__(self, **kwds):
		kwds.setdefault('extent', default_extent)
		doc = win_get_dummy_doc()
		win = ui.CreateView(doc)
		#win.CreateWindow(win_none, 0, win_style, (0, 0, 100, 100))
		win.CreateWindow(win_none, ui.AFX_IDW_PANE_FIRST, win_style, (0, 0, 100, 100))
		GScrollableView.__init__(self, _win = win)
		self.set(**kwds)

	def get_hscrolling(self):
		return self._win.GetStyle() & wc.WS_HSCROLL != 0
	
	def get_vscrolling(self):
		return self._win.GetStyle() & wc.WS_VSCROLL != 0
	
	def set_hscrolling(self, x):
		self._win_set_flag(x, wc.WS_HSCROLL)
	
	def set_vscrolling(self, x):
		self._win_set_flag(x, wc.WS_VSCROLL)
	
	def get_line_scroll_amount(self):
		return self._line_scroll_amount
	
	def get_extent(self):
		return self._win.GetTotalSize()
	
	def set_extent(self, extent):
		self._win_update_scroll_sizes(extent)
	
	def get_scroll_offset(self):
		return self._win.GetScrollPosition()
	
	def set_scroll_offset(self, p):
		px, py = p
		ex, ey = self.extent
		vx, vy = self.content_size
		xmax = max(0, ex - vx)
		ymax = max(0, ey - vy)
		x = max(0, min(px, xmax))
		y = max(0, min(py, ymax))
		self._win.ScrollToPosition((x, y))
	
	def set_bounds(self, bounds):
		GScrollableView.set_bounds(self, bounds)
		extent = self._win.GetTotalSize()
		self._win_update_scroll_sizes(extent)
	
	def _invalidate_rect(self, r):
		win = self._win
		s = win.GetScrollPosition()
		self._win.InvalidateRect(offset_rect_neg(r, s))

	def local_to_global(self, p):
		win = self._win
		q = sub_pt(p, win.GetScrollPosition())
		return win.ClientToScreen(q)
	
	def global_to_local(self, g):
		win = self._win
		q = win.ScreenToClient(g)
		return add_pt(q, win.GetScrollPosition())

#	def global_to_local(self, g):
#		win = self._win
#		l = win.ScreenToClient(g)
#		s = win.GetScrollPosition()
#		q = add_pt(l, s)
#		print "ScrollableView.global_to_local: g =", g, "l =", l, "s =", s, "q =", q ###
#		return q

	def _win_update_scroll_sizes(self, extent):
		ph = self.h_page_scroll_amount()
		pv = self.v_page_scroll_amount()
		ls = self.line_scroll_amount
		self._win.SetScrollSizes(wc.MM_TEXT, extent, (ph, pv), ls)
	
	def OnDraw(self, dc):
		#print "ScrollableView.OnDraw" ###
		update_rect = dc.GetClipBox()
		canvas = Canvas._from_win_dc(dc)
		self.draw(canvas, update_rect)

	def _win_prepare_dc(self, dc, pinfo = None):
		self._win.OnPrepareDC(dc, None)

		


