#--------------------------------------------------------------------
#
#   PyGUI - Window - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui, win32api as api
from GUI import export
from GUI import WinUtils 
from GUI.Geometry import rect_size, sub_pt
from GUI import application
from GUI.Exceptions import Cancel
from GUI.WinEvents import win_message_to_event
from GUI.WinMenus import MenuBar, win_id_to_command
from GUI.GMenus import search_list_for_key
from GUI import Component
from GUI.GWindows import Window as GWindow

#--------------------------------------------------------------------

capabilities = ('hidable', 'zoomable', 'resizable', 'movable', 'closable')

win_defaults = {
	'standard':        (1, 1, 1, 1, 1),
	'nonmodal_dialog': (1, 0, 0, 1, 1),
	'modal_dialog':    (0, 0, 0, 1, 1),
	'alert':           (0, 0, 0, 1, 1),
	'fullscreen':      (0, 0, 0, 0, 0),
}

win_base_flags = wc.WS_CLIPCHILDREN
win_border_flags = wc.WS_DLGFRAME

win_capability_flags = {
	'hidable': wc.WS_MINIMIZEBOX | wc.WS_SYSMENU,
	'zoomable': wc.WS_MAXIMIZEBOX | wc.WS_SYSMENU,
	'resizable': wc.WS_THICKFRAME,
	'movable': wc.WS_BORDER,
	'closable': wc.WS_SYSMENU,
}

win_no_menu_styles = ('nonmodal_dialog', 'modal_dialog',
	'alert', 'fullscreen')

win_ex_flags = 0 #wc.WS_EX_WINDOWEDGE
win_no_ex_flags = wc.WS_EX_CLIENTEDGE

def win_calculate_flags(style, kwds):
	#  Calculate window flags from the options present in kwds, and
	#  fill in kwds with default values for missing options that need
	#  to be passed to the base class constructor.
	flags = win_base_flags
	if style != 'fullscreen':
		flags |= win_border_flags
	try:
		defaults = win_defaults[style]
	except KeyError:
		raise ValueError("Invalid window style '%s'" % style)
	for name, default in zip(capabilities, defaults):
		value = kwds.pop(name, default)
		if name == 'closable':
			kwds[name] = value
		if value:
			flags |= win_capability_flags[name]
	return flags

#def win_adjust_flags(flags, kwds, option_name, opt_flags):
#	option = kwds.pop(option_name, None)
#	if option is not None:
#		if option:
#			flags |= opt_flags
#		else:
#			flags &= ~opt_flags
#	return flags

def win_next_wnd(wnd):
	wnd = getattr(wnd, '_win', wnd)
	#print "win_next_wnd:", wnd ###
	return  wnd.GetWindow(wc.GW_HWNDNEXT)

#--------------------------------------------------------------------

class Window(GWindow):

	_win_hooks_events = True
	_win_has_menubar = True
	_win_captures_mouse = True

	_win_need_menubar_update = True
	_win_saved_target = False
	_win_fullscreen = False

	def __init__(self, **kwds):
		style = kwds.get('style', 'standard')
		flags = win_calculate_flags(style, kwds)
		#if style == 'fullscreen':
		#	rect = WinUtils.win_screen_rect
		#else:
		rect = (0, 0, self._default_width, self._default_height)
		frame = ui.CreateFrame()
		frame.CreateWindow(None, "New Window", 0, rect)
		hwnd = frame.GetSafeHwnd()
		#api.SetClassLong(hwnd, wc.GCL_HBRBACKGROUND, win_bg_hbrush)
		api.SetClassLong(hwnd, wc.GCL_HBRBACKGROUND, 0)
#		print "Window: Setting style:" ###
#		win_deconstruct_style(flags) ###
		frame.ModifyStyle(-1, flags)
#		print "Window: Style is now:" ###
#		win_deconstruct_style(frame.GetStyle()) ###
		frame.ModifyStyleEx(win_no_ex_flags, win_ex_flags)
		if style == 'fullscreen':
			self._win_fullscreen = True
		frame.HookMessage(self._win_wm_initmenu, wc.WM_INITMENU)
		self._win = frame
		if style in win_no_menu_styles:
			self._win_has_menubar = False
		else:
			self._win_set_empty_menubar()
		kwds['closable'] = flags & wc.WS_CAPTION <> 0
		GWindow.__init__(self, _win = frame, **kwds)
	
	def OnPaint(self):
		win = self._win
		dc, ps = win.BeginPaint()
		rect = win.GetClientRect()
		dc.FillSolidRect(rect, WinUtils.win_bg_color)
		if self._win_has_menubar:
			l, t, r, b = rect
			dc.Draw3dRect((l, t, r + 1, t + 2),
				WinUtils.win_color3dshadow, WinUtils.win_color3dhilight)
		win.EndPaint(ps)

	def _win_install_event_hooks(self): 
		self._win.HookMessage(self._wm_activate, wc.WM_ACTIVATE)
		#self._win.HookMessage(self._wm_setfocus, wc.WM_SETFOCUS)
		self._win.HookMessage(self._wm_windowposchanging, wc.WM_WINDOWPOSCHANGING)
		self._win.HookMessage(self._wm_windowposchanged, wc.WM_WINDOWPOSCHANGED)
		GWindow._win_install_event_hooks(self)
	
	def _wm_activate(self, msg):
		wParam = msg[2]
		#print "Window._wm_activate:", msg ###
		#print "...wParam =", wParam ###
		if wParam == wc.WA_INACTIVE:
			#print "Window: Deactivating:", self ###
			try:
				target = ui.GetFocus()
				#print "...target =", target ###
			except ui.error, e:
				#print "...no target", e ###
				target = None
			if isinstance(target, Component) and target is not self:
				#print "...saving target", target ###
				self._win_saved_target = target

	def _win_wm_setfocus(self, msg):
		#print "Window._win_wm_setfocus:", self ###
		target = self._win_saved_target
		if target and target.window == self:
			#print "...restoring target", target ###
			target._win.SetFocus()
			self._win_saved_target = None
		else:
			GWindow._win_wm_setfocus(self, msg)
	
	def get_target(self):
		if self._win_is_active():
			try:
				target = ui.GetFocus()
			except ui.error:
				target = None
			if target and isinstance(target, Component):
				return target
		return self._saved_target or self
	
	def _win_is_active(self):
		try:
			active_win = ui.GetActiveWindow()
		except ui.error:
			active_win = None
		return active_win is self

#	def _wm_setfocus(self, *args):
#		print "Window._wm_setfocus:", args ###

	def _wm_windowposchanging(self, message):
		#print "Window._wm_windowposchanging"
		self._win_old_size = rect_size(self._bounds)
		#print "...old size =", self._win_old_size
	
	def _wm_windowposchanged(self, message):
		#print "Window._wm_windowposchanged"
		old_size = self._win_old_size
		new_bounds = self._win_get_actual_bounds()
		self._bounds = new_bounds
		new_size = rect_size(new_bounds)
		#print "...new size =", new_size
		if old_size != new_size:
			self._resized(sub_pt(new_size, old_size))
	
	def _win_set_empty_menubar(self):
		#  A completely empty menu bar collapses to zero height, and
		#  controlling the window bounds is too complicated if the
		#  menu bar comes and goes, so we add a dummy item to it.
		menubar = MenuBar()
		menubar.win_menu.AppendMenu(0, 0, "")
		self._win.SetMenu(menubar.win_menu)
		self._win_menubar = menubar
	
	def get_title(self):
		return self._win.GetWindowText()
	
	def set_title(self, x):
		self._win.SetWindowText(x)

	def get_visible(self):
		return self._win.IsWindowVisible()
	
	def set_visible(self, x):
		#print "Window.set_visible:", x, self ###
		if x:
			self._win_update_menubar()
			self._win.ShowWindow()
		else:
			self._win.ShowWindow(wc.SW_HIDE)
	
	def _show(self):
		self._win_update_menubar()
		win = self._win
		if self._win_fullscreen:
			win.ShowWindow(wc.SW_SHOWMAXIMIZED)
#		win.SetWindowPos(wc.HWND_TOP, (0, 0, 0, 0),
#			wc.SWP_NOMOVE | wc.SWP_NOSIZE | wc.SWP_SHOWWINDOW)
		win.ShowWindow(wc.SW_SHOWNORMAL)
		win.SetActiveWindow()
	
#	def get_bounds(self):
#		win = self._win
#		r = win.ClientToScreen(win.GetClientRect())
#		return r

	def _win_get_actual_bounds(self):
		win = self._win
		return win.ClientToScreen(win.GetClientRect())
	
	def _win_move_window(self, rect):
		win = self._win
		l, t, r, b = win.CalcWindowRect(rect)
		if self._win_has_menubar:
			t -= WinUtils.win_menubar_height
		self._win.MoveWindow((l, t, r, b))
	
	def set_menus(self, x):
		GWindow.set_menus(self, x)
		self._win_menus_changed()

	def _stagger(self):
		#print "Window._stagger:", self ###
		win = win_next_wnd(self._win)
		while win and not (isinstance(win, Window) and win.visible):
			#print "...win =", win ###
			win = win_next_wnd(win)
		if win:
			l, t, r, b = win._win.GetWindowRect()
			hwnd = self._win.GetSafeHwnd()
			gui.SetWindowPos(hwnd, 0, l + 20, t + 20, 0, 0,
				wc.SWP_NOSIZE | wc.SWP_NOZORDER)

	def OnClose(self):
		#print "Window:", self, "OnClose"
		try:
			self.close_cmd()
		except Cancel:
			pass
		except:
			application().report_error()
		
	def _win_menus_changed(self):
		self._win_need_menubar_update = True
		if self.visible:
			self._win_update_menubar()
	
	def _win_update_menubar(self):
		#print "Window._win_update_menubar:", self ###
		if self._win_need_menubar_update:
			all_menus = application()._effective_menus_for_window(self)
			self._all_menus = all_menus
			if self._win_has_menubar:
				if all_menus:
					menubar = MenuBar()
					for menu in all_menus:
						menubar.append_menu(menu)
					self._win.SetMenu(menubar.win_menu)
					self._win_menubar = menubar
				else:
					self._win_set_empty_menubar()
			self._win_need_menubar_update = False
	
	def _win_wm_initmenu(self, message):
		#print "Window._win_wm_initmenu:", self ###
		self._win_perform_menu_setup()
	
	def _win_perform_menu_setup(self):
		#print "Window._win_perform_menu_setup:", self ###
		application()._perform_menu_setup(self._all_menus)
	
	def _win_menu_command(self, id):
		command = win_id_to_command(id)
		if command:
			application().dispatch_menu_command(command)
			return True
		else:
		    return False
	
	def _win_possible_menu_key(self, key, shift, option):
		self._win_perform_menu_setup()
		command = search_list_for_key(self._all_menus, key, shift, option)
		if command:
			application().dispatch_menu_command(command)
			return True
	
	def _screen_rect(self):
		return WinUtils.win_screen_rect
	
	def modal_event_loop(self):
		disabled = []
		for window in application().windows:
			if window is not self:
				if not window._win.EnableWindow(False):
					#print "Window.modal_event_loop: disabled", window.title ###
					disabled.append(window)
		status = self._win.RunModalLoop(0)
		if status:
			print "Window._modal_event_loop:", self, "status =", status ###
			#raise Cancel
		for window in disabled:
			#print "Window.modal_event_loop: enabling", window.title ###
			window._win.EnableWindow(True)
		if status <> 0: ###
			from GUI.Exceptions import InternalError ###
			raise InternalError("RunModalLoop returned %s" % status) ###
	
	def exit_modal_event_loop(self):
		self._win.EndModalLoop(0)

export(Window)
