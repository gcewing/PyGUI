#--------------------------------------------------------------------
#
#   PyGUI - Component - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui, win32api as api

from GUI import export
from GUI.Geometry import sub_pt
from GUI import application
from GUI.WinUtils import win_none, win_event_messages
from GUI.WinEvents import win_message_to_event, win_prev_key_state
from GUI.Exceptions import Cancel
from GUI.GComponents import Component as GComponent, transform_coords

win_swp_flags = wc.SWP_NOACTIVATE | wc.SWP_NOZORDER
win_sws_flags = win_swp_flags | wc.SWP_NOMOVE

#  Virtual key code to menu key char
win_menu_key_map = {
	0xc0: '`',
	0xbd: '-',
	0xbb: '=',
	0xdb: '[',
	0xdd: ']',
	0xba: ';',
	0xde: "'",
	0xbc: ',',
	0xbe: '.',
	0xbf: '/',
	0xdc: '\\',
}

#  Virtual key codes of modifier keys
win_virt_modifiers = (0x10, 0x11, 0x12, 0x14, 0x90)

#  Translate virtual key code to menu key char
def win_translate_virtual_menu_key(virt):
	if 0x41 <= virt <= 0x5a or 0x30 <= virt <= 0x39:
		return chr(virt)
	else:
		return win_menu_key_map.get(virt)

#--------------------------------------------------------------------

class Component(GComponent):

	_has_local_coords = True
	_win_hooks_events = False
	_win_transparent = False
	_win_captures_mouse = False
	
	_h_scroll_offset = 0
	_v_scroll_offset = 0
	_win_tracking_mouse = False

	def __init__(self, _win, **kwds):
		if self._win_transparent:
			_win.ModifyStyleEx(0, wc.WS_EX_TRANSPARENT, 0)
		self._win = _win
		self._bounds = self._win_get_actual_bounds()
		_win.AttachObject(self)
		self._win_install_event_hooks()
		GComponent.__init__(self, **kwds)
	
	def destroy(self):
		GComponent.destroy(self)
		wo = self._win
		if wo:
			wo.AttachObject(None)
			wo.ShowWindow(wc.SW_HIDE)
			application()._win_recycle(wo)
			#self._win = None
	
	def _win_get_flag(self, flag):
		return self._win.GetStyle() & flag != 0
	
	def _win_set_flag(self, b, flag, swp_flags = 0):
		if b:
			state = flag
		else:
			state = 0
		self._win.ModifyStyle(flag, state, swp_flags)
	
	def _win_set_ex_flag(self, b, flag, swp_flags = 0):
		if b:
			state = flag
		else:
			state = 0
		self._win.ModifyStyleEx(flag, state, swp_flags)
	
	def _change_container(self, new_container):
		GComponent._change_container(self, new_container)
		if new_container:
			win_new_parent = new_container._win
		else:
			win_new_parent = win_none
		hwnd = self._win.GetSafeHwnd()
		gui.SetParent(hwnd, win_new_parent.GetSafeHwnd())
		if new_container:
			self._win_move_window(self._bounds)
	
	def _win_install_event_hooks(self):
		def hook(message):
			return self._win_event_message(message)
		win = self._win
		for msg in win_event_messages:
			win.HookMessage(hook, msg)
		win.HookMessage(self._win_wm_setfocus, wc.WM_SETFOCUS)
		win.HookMessage(self._win_wm_killfocus, wc.WM_KILLFOCUS)
	
	def _win_wm_setfocus(self, msg):
		#print "Component._win_wm_setfocus:", self ###
		self.targeted()
		return True
	
	def targeted(self):
		pass
	
	def _win_wm_killfocus(self, msg):
		#print "Component._win_wm_killfocus:", self ###
		self.untargeted()
		return True
	
	def untargeted(self):
		pass
	
	def _win_on_ctlcolor(self, dc, typ):
		pass
	
#	def OnCtlColor(self, dc, comp, typ):
#		#print "Component.OnCtlColor" ###
#		meth = getattr(comp, '_win_on_ctlcolor', None)
#		if meth:
#			return meth(dc, typ)

	def get_bounds(self):
		return self._bounds
	
	def set_bounds(self, rect):
		self._win_move_window(rect)
		self._win_change_bounds(rect)
	
	def _win_change_bounds(self, rect):
		l0, t0, r0, b0 = self._bounds
		l1, t1, r1, b1 = rect
		w0 = r0 - l0
		h0 = b0 - t0
		w1 = r1 - l1
		h1 = b1 - t1
		self._bounds = rect
		if w0 != w1 or h0 != h1:
			self._resized((w1 - w0, h1 - h0))
	
	def _win_move_window(self, bounds):
		container = self.container
		if container:
			rect = container._win_adjust_bounds(bounds)
			self._win.MoveWindow(rect)
	
	def _win_adjust_bounds(self, bounds):
		#  Scrollable views override this to adjust for the scroll offset.
		return bounds
	
	def _win_get_actual_bounds(self):
		win = self._win
		parent = win.GetParent()
		sbounds = win.GetWindowRect()
		return parent._win.ScreenToClient(sbounds)

	def become_target(self):
		#print "Component.become_target:", self ###
		window = self.window
		if window:
			if window._win_is_active():
				#print "...setting focus" ###
				self._win.SetFocus()
			else:
				#print "...saving focus in", window ###
				window._win_saved_target = self
	
	def invalidate_rect(self, r):
		#print "Component.invalidate_rect:", self, r ###
		self._invalidate_rect(r)
		if self._win_transparent:
			cont = self.container
			if cont:
				cont.invalidate_rect(self.local_to_container(r))
	
	def _invalidate_rect(self, r):
		self._win.InvalidateRect(r)

	def local_to_global(self, p):
		return self._win.ClientToScreen(p)
	
	def global_to_local(self, p):
		return self._win.ScreenToClient(p)
	
	def container_to_local(self, p):
		return transform_coords(self.container, self, p)
	
	def local_to_container(self, p):
		return transform_coords(self, self.container, p)

	def _win_event_message(self, message):
		try:
			if 0:
				from WinUtils import win_message_name ###
				print "Component._win_event_message: %s 0x%08x 0x%08x" % ( ###
					win_message_name(message[1]),
					message[2] & 0xffffffff,
					message[3] & 0xffffffff) ###
			event = win_message_to_event(message, self)
			kind = event.kind
			if kind.startswith('key') and message[2] in win_virt_modifiers:
				#  Do not produce Events for modifier keys
				return True
			if kind == 'mouse_down' and self._win_captures_mouse:
				self._win.SetCapture()
			if self._win_tracking_mouse:
				if 'mouse' in kind:
					self._win_mouse_event = event
					api.PostQuitMessage(0)
				pass_message = False
			else:
				if kind == 'key_down' and event.control and event.char:
					key = win_translate_virtual_menu_key(message[2])
					top = self._win.GetTopLevelFrame()
					if top._win_possible_menu_key(key, event.shift, event.option):
						return False
				pass_message = not self._event_custom_handled(event)
			if kind == 'mouse_up' and self._win_captures_mouse:
				self._win.ReleaseCapture()
#			#<<<
#			if kind.startswith('key'):
#				if pass_message:
#					print "Component._win_event_message: passing", event ###
#				else:
#					print "Component._win_event_message: absorbing", event ###
#			#>>>
			return pass_message
		except Cancel:
			pass
		except:
			application().report_error()
#			print "Component._win_event_message: Posting quit message with 1" ###
#			api.PostQuitMessage(1)

	def _win_dump_flags(self):
		from WinUtils import win_deconstruct_style, win_deconstruct_style_ex
		print "%s.%s: style:" % (self.__class__.__module__, self.__class__.__name__)
		win_deconstruct_style(self._win.GetStyle())
		win_deconstruct_style_ex(self._win.GetExStyle())

#	def PreTranslateMessage(self, message):
#		print "Component.PreTranslateMessage:", self, \
#			message[0], win_message_name(message[1]), \
#			message[2]
#
#from WinUtils import win_message_name

export(Component)
