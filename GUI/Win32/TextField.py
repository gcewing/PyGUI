#--------------------------------------------------------------------
#
#   PyGUI - TextField - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI import export
from GUI.StdFonts import application_font
from GUI.WinUtils import win_none
from GUI.GTextFields import TextField as GTextField

win_vpad = 5
win_style = wc.WS_VISIBLE | wc.WS_CLIPSIBLINGS | wc.ES_AUTOHSCROLL # | wc.WS_TABSTOP
win_ex_style = wc.WS_EX_CLIENTEDGE
win_multiline_style = wc.ES_MULTILINE | wc.ES_AUTOVSCROLL
win_password_style = wc.ES_PASSWORD

win_just_mask = wc.ES_LEFT | wc.ES_CENTER | wc.ES_RIGHT

win_just_flags = {
	'l': wc.ES_LEFT,
	'c': wc.ES_CENTER,
	'r': wc.ES_RIGHT,
}

class TextField(GTextField):

	_pass_key_events_to_platform = True
	
	_win_setting_text = False

	def __init__(self, **kwds):
		font = kwds.setdefault('font', application_font)
		multiline = kwds.setdefault('multiline', False)
		password = kwds.pop('password', False)
		self._multiline = multiline
		self._password = password
		h = self._calc_height(font)
		flags = win_style
		if multiline:
			flags |= win_multiline_style
		if password:
			flags |= win_password_style
		win = ui.CreateEdit()
		#  Border can get lost if we construct it with too big a rect, so
		#  we set the initial size after creation.
		win.CreateWindow(flags, (0, 0, 0, 0), win_none, 0)
		win.ModifyStyleEx(0, win_ex_style)
		win.MoveWindow((0, 0, 100, h))
		GTextField.__init__(self, _win = win, **kwds)
	
	def get_text(self):
		return self._win.GetWindowText().replace("\r\n", "\n")
	
	def set_text(self, x):
		self._win_setting_text = True
		try:
			self._win.SetWindowText(x.replace("\n", "\r\n"))
		finally:
			self._win_setting_text = False
	
	def set_just(self, x):
		self._just = x
		try:
			flags = win_just_flags[x[:1]]
		except KeyError:
			raise ValueError("Invalid TextField justification %r" % x)
		self._win.ModifyFlags(win_just_mask, flags)

	def get_selection(self):
		sel = self._win.GetSel()
		if self._multiline:
			sel = self._win_adjust_sel(sel, -1)
		return sel
	
	def set_selection(self, sel):
		if self._multiline:
			sel = self._win_adjust_sel(sel, 1)
		self._win.SetSel(*sel)
		self.become_target()
	
	def _win_adjust_sel(self, sel, d):
		text = self._win.GetWindowText()
		if d > 0:
			text = text.replace("\r\n", "\n")
			nl = "\n"
		else:
			nl = "\r\n"
		def adj(x):
			return x + d * text.count(nl, 0, x)
		return map(adj, sel)

	def get_multiline(self):
		return self._multiline

	def get_password(self):
		return self._password

	def _tab_in(self):
		self.select_all()

	def key_down(self, event):
		#print "TextField.key_down" ###
		if event.char == "\t":
			self.pass_event_to_next_handler(event)
		else:
			GTextField.key_down(self, event)
	
	def _en_change(self, *args):
		#print("TextField._en_change")
		if not self._win_setting_text:
			self.do_text_changed_action()

	def get_editable(self):
		return not self._win.GetReadOnly()
	
	def set_editable(self, x):
		self._win.SetReadOnly(not x)

export(TextField)
