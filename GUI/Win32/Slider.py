#--------------------------------------------------------------------
#
#   PyGUI - Slider - Win32
#
#--------------------------------------------------------------------

from __future__ import division
import win32con as wc, win32ui as ui
from GUI import export
from GUI.WinUtils import win_none
from GUI.GSliders import Slider as GSlider

win_base_flags = wc.WS_CHILD | wc.WS_VISIBLE

win_styles = {
	'h': 0x0, # TBS_HORZ | TBS_BOTTOM
	#'v': 0x6, # TBS_VERT | TBS_LEFT
	'v': 0x2, # TBS_VERT | TBS_RIGHT
}

win_no_ticks = 0x10 # TBS_NOTICKS
win_continuous_range = 10000

class Slider(GSlider):

	#_win_transparent = True
	_default_breadth = 20

	_min_value = 0.0
	_max_value = 1.0
	_discrete = False
	_ticks = 0
	_live = True

	def __init__(self, orient, **kwds):
		win = ui.CreateSliderCtrl()
		win_flags = win_base_flags | win_no_ticks
		try:
			style = win_styles[orient]
		except KeyError:
			raise ValueError("Invalid Slider orientation %r" % orient)
		l = self._default_length
		b = self._default_breadth
		if orient == 'h':
			rect = (0, 0, l, b)
		else:
			rect = (0, 0, b, l)
		win.CreateWindow(style | win_flags, rect, win_none, 0)
		win.SetRange(0, win_continuous_range)
		GSlider.__init__(self, _win = win, **kwds)
	
	def get_value(self):
		win = self._win
		p = win.GetPos()
		q = win.GetRangeMax()
		x0 = self._min_value
		x1 = self._max_value
		return x0 + (x1 - x0) * p / q
	
	def set_value(self, x):
		win = self._win
		x0 = self._min_value
		x1 = self._max_value
		q = win.GetRangeMax()
		p = int(round(q * (x - x0) / (x1 - x0)))
		self._win.SetPos(p)
	
	def get_min_value(self):
		return self._min_value
	
	def set_min_value(self, x):
		self._min_value = x
		self._win_update_range()
	
	def get_max_value(self):
		return self._max_value
	
	def set_max_value(self, x):
		self._max_value = x
		self._win_update_range()
	
	def get_ticks(self):
		return self._ticks
	
	def set_ticks(self, n):
		self._ticks = n
		self._win_update_ticks()
	
	def get_discrete(self):
		return self._discrete
	
	def set_discrete(self, d):
		if self._discrete != d:
			self._discrete = d
			self._win_update_range()
	
	def get_live(self):
		return self._live
	
	def set_live(self, x):
		self._live = x
	
	def _win_update_range(self):
		if self._discrete:
			x1 = max(0, self._ticks - 1)
		else:
			x1 = win_continuous_range
		self._win.SetRange(0, x1)
		self._win_update_ticks()
	
	def _win_update_ticks(self):
		#print "Slider._win_update_ticks" ###
		win = self._win
		n = self._ticks
		if n >= 2:
			if self._discrete:
				f = 1
			else:
				f = int(round(win_continuous_range / (n - 1)))
			win.ModifyStyle(win_no_ticks, 0)
			win.ClearTics(False)
			for i in xrange(n + 1):
				win.SetTic(int(round(i * f)))
		else:
			win.ModifyStyle(0, win_no_ticks)

	def _win_wm_scroll(self, code):
		#print "Slider._win_wm_scroll:", code ###
		if self._live:
			report = code != 8
		else:
			report = code == 8
		if report:
			self.do_action()

	def _win_on_ctlcolor(self, dc, typ):
		#print "Slider._win_on_ctlcolor:", self ###
		return self._win.OnCtlColor(dc, self._win, typ)

	def key_down(self, event):
		k = event.key
		if k == 'left_arrow' or k == 'up_arrow':
			self._nudge_value(-1)
		elif k == 'right_arrow' or k == 'down_arrow':
			self._nudge_value(1)
		else:
			GSlider.key_down(self, event)

	def _nudge_value(self, d):
		if not self.discrete:
			d *= (win_continuous_range // 100)
		win = self._win
		p = win.GetPos()
		win.SetPos(p + d)
		self.do_action()

export(Slider)
