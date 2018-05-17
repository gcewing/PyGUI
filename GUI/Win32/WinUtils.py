#--------------------------------------------------------------------
#
#   PyGUI - Win32 - Utilities
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui, win32api as api
from win32api import HIWORD, LOWORD
from GUI import application
from GUI.Exceptions import Cancel, InternalError

win_dlog_class = "#32770"
win_color3dhilight = api.GetSysColor(wc.COLOR_3DHILIGHT)
win_color3dlight = api.GetSysColor(wc.COLOR_3DLIGHT)
win_color3dface = api.GetSysColor(wc.COLOR_3DFACE)
win_color3dshadow = api.GetSysColor(wc.COLOR_3DSHADOW)
win_menubar_height = api.GetSystemMetrics(wc.SM_CYMENU)
win_bg_color = api.GetSysColor(wc.COLOR_3DFACE)
win_screen_width = api.GetSystemMetrics(wc.SM_CXFULLSCREEN)
win_screen_height = api.GetSystemMetrics(wc.SM_CYFULLSCREEN)
win_screen_rect = (0, 0, win_screen_width, win_screen_height)

#win_bg_brush = ui.CreateBrush(wc.BS_SOLID, win_color3dface, 0)
#win_bg_hbrush = win_bg_brush.GetSafeHandle()

#  An empty brush for not painting anything with
win_null_brush = ui.CreateBrush(wc.BS_NULL, 0, 0)
win_null_hbrush = win_null_brush.GetSafeHandle()

#  All components hook the following messages

win_event_messages = (
	wc.WM_KEYDOWN, wc.WM_KEYUP,
	wc.WM_SYSKEYDOWN, wc.WM_SYSKEYUP,
	wc.WM_MOUSEMOVE,
	wc.WM_LBUTTONDOWN, wc.WM_LBUTTONDBLCLK, wc.WM_LBUTTONUP,
	wc.WM_MBUTTONDOWN, wc.WM_MBUTTONDBLCLK, wc.WM_MBUTTONUP,
	wc.WM_RBUTTONDOWN, wc.WM_RBUTTONDBLCLK, wc.WM_RBUTTONUP,
	#wc.WM_MOUSELEAVE,
)

#  Dummy CWnd for use as parent of containerless components.
#  Also used as the main frame of the CWinApp.

win_none = ui.CreateFrame()
win_none.CreateWindow(None, "", 0, (0, 0, 10, 10))

win_plain = ui.CreateWnd()
win_plain.CreateWindow(None, None, 0, (0, 0, 10, 10), win_none, 0)
win_plain_class = gui.GetClassName(win_plain.GetSafeHwnd())

#--------------------------------------------------------------------

win_command_map = {
	0: '_win_bn_clicked', # BN_CLICKED
	wc.CBN_SELCHANGE: '_cbn_sel_change',
	wc.EN_CHANGE: '_en_change',
}

class WinMessageReflector(object):

	def _win_install_event_hooks(self, win):
		win.HookMessage(self._win_wm_scroll, wc.WM_HSCROLL)
		win.HookMessage(self._win_wm_scroll, wc.WM_VSCROLL)

#
#  Disabled for now because overriding control colours
#  doesn't seem to work properly on XP.
#
#	def OnCtlColor(self, dc, comp, typ):
#		#print "WinMessageReflector.OnCtlColor" ###
#		meth = getattr(comp, '_win_on_ctlcolor', None)
#		if meth:
#			return meth(dc, typ)

	def _win_wm_scroll(self, message):
		#print "WinMessageReflector._win_wm_scroll:", self, message ###
		wParam = message[2]
		code = wParam & 0xffff
		lParam = message[3]
		self._forward_reflected_message(lParam, '_win_wm_scroll', code)

	def OnCommand(self, wParam, lParam):
		#print "WinMessageReflector.OnCommand: code = 0x%04x 0x%04x lParam = 0x%08x" % (
		#	HIWORD(wParam), LOWORD(wParam), lParam)
		try:
			code = HIWORD(wParam)
			id = LOWORD(wParam)
			if id:
				if self._win_menu_command(id):
					return
			name = win_command_map.get(code)
			if name:
				self._forward_reflected_message(lParam, name)
		except Cancel:
			pass
		except:
			application().report_error()

	def _forward_reflected_message(self, lParam, method_name, *args):
		wnd = ui.CreateWindowFromHandle(lParam)
		meth = getattr(wnd, method_name, None)
		if meth:
			meth(*args)

	def _win_menu_command(self, id):
		raise InternalError("_win_menu_command called on non-window: %r" % self)

win_none_wrapper = WinMessageReflector()
win_none_wrapper._win = win_none
win_none_wrapper._win_install_event_hooks(win_none)
win_none.AttachObject(win_none_wrapper)

#--------------------------------------------------------------------
#
#   Debugging routines
#

win_message_names = {}

win_exclude_names = ["WM_MOUSEFIRST"]

for name, value in wc.__dict__.iteritems():
	if name.startswith("WM_") and name not in win_exclude_names:
		win_message_names[value] = name

def win_message_name(num):
	return win_message_names.get(num) or num

def dump_flags(flags):
	for name in wc.__dict__.iterkeys():
		if name.startswith("WS_") and not name.startswith("WS_EX"):
			value = wc.__dict__[name]
			if flags & value:
				print "%20s = 0x%08x" % (name, value & 0xffffffffL)
		
def win_deconstruct_style(flags):
	win_do_deconstruct_style(flags, "WS_", "WS_EX_")

def win_deconstruct_style_ex(flags):
	win_do_deconstruct_style(flags, "WS_EX_")

def win_do_deconstruct_style(flags, prefix, not_prefix = None):
	d = wc.__dict__
	for name in d.iterkeys():
		if name.startswith(prefix):
			if not not_prefix or not name.startswith(not_prefix):
				value = d[name]
				if value and flags & value == value:
					print "%25s 0x%08x" % (name, value)
