#
#   Python GUI - Text Editor - Win32
#

from __future__ import division
import win32con as wc, win32ui as ui
from GUI import export
from GUI.GTextEditors import TextEditor as GTextEditor
from GUI.WinUtils import win_none
from GUI.StdFonts import application_font

PFM_TABSTOPS = 0x10
MAX_TAB_STOPS = 32
LOGPIXELSX = 88

ui.InitRichEdit()

class TextEditor(GTextEditor):

	_pass_key_events_to_platform = True

	def __init__(self, scrolling = 'hv', **kwds):
		win_style = ui.AFX_WS_DEFAULT_VIEW #| wc.WS_HSCROLL | wc.WS_VSCROLL
		win = ui.CreateRichEditView()
		ctl = win.GetRichEditCtrl()
		self._win_ctl = ctl
		if 'h' in scrolling:
			win.SetWordWrap(0) # Must do before CreateWindow
		win.CreateWindow(win_none, 1, win_style, (0, 0, 100, 100))
		#if 'v' not in scrolling:
			# Disabled because it doesn't work properly -- auto-scrolling is prevented
			# but a vertical scroll bar still appears when text goes past bottom of window.
			#ctl.SetOptions(wc.ECOOP_XOR, wc.ECO_AUTOVSCROLL) # Must do after CreateWindow
		ctl.SetOptions(wc.ECOOP_XOR, wc.ECO_NOHIDESEL)
		win.ShowScrollBar(wc.SB_BOTH, False)
		# We allow automatic scroll bar show/hide -- resistance is futile
		win.ShowWindow()
		kwds.setdefault('font', application_font)
		GTextEditor.__init__(self, _win = win, **kwds)
#		self.tab_spacing = self.font.width("X") * 4 ###

	def get_selection(self):
		return self._win.GetSel()
	
	def set_selection(self, value):
		self._win.SetSel(*value)
	
	def get_text(self):
		return self._win.GetWindowText()
	
	def set_text(self, text):
		self._win.SetWindowText(text)

	def get_text_length(self):
		return self._win.GetTextLength()

	def get_font(self):
		return self._font
	
	def set_font(self, x):
		self._font = x
		self._win.SetFont(x._win_font)
		self.invalidate()

	def get_tab_spacing(self):
		pf = self._win_ctl.GetParaFormat()
		tabs = pf[8]
		if tabs:
			return tabs[0] // 20
		else:
			return 36
	
	def set_tab_spacing(self, x):
		dc = self._win.GetDC()
		dpi = dc.GetDeviceCaps(LOGPIXELSX)
		mask = PFM_TABSTOPS
		twips = 1440 * x / dpi
		tabs = [int(round((i + 1) * twips)) for i in xrange(MAX_TAB_STOPS)]
		pf = (mask, 0, 0, 0, 0, 0, 0, tabs)
		old_sel = self.selection
		self.select_all()
		self._win_ctl.SetParaFormat(pf)
		self.selection = old_sel

export(TextEditor)
