#--------------------------------------------------------------------
#
#   PyGUI - Event utilities - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32api as api, win32gui as gui, win32ui as ui
from GUI import Event

win_message_map = {
	wc.WM_KEYDOWN:        ('key_down',    None),
	wc.WM_KEYUP:          ('key_up',      None),
	wc.WM_SYSKEYDOWN:     ('key_down',    None),
	wc.WM_SYSKEYUP:       ('key_up',      None),
	wc.WM_MOUSEMOVE:      ('mouse_move',  None),
	wc.WM_LBUTTONDOWN:    ('mouse_down', 'left'),
	wc.WM_LBUTTONDBLCLK:  ('mouse_down', 'left'),
	wc.WM_LBUTTONUP:      ('mouse_up',   'left'),
	wc.WM_MBUTTONDOWN:    ('mouse_down', 'middle'),
	wc.WM_MBUTTONDBLCLK:  ('mouse_down', 'middle'),
	wc.WM_MBUTTONUP:      ('mouse_up',   'middle'),
	wc.WM_RBUTTONDOWN:    ('mouse_down', 'right'),
	wc.WM_RBUTTONDBLCLK:  ('mouse_down', 'right'),
	wc.WM_RBUTTONUP:      ('mouse_up',   'right'),
}

win_special_keys = {
	0x70: 'f1',
	0x71: 'f2',
	0x72: 'f3',
	0x73: 'f4',
	0x74: 'f5',
	0x75: 'f6',
	0x76: 'f7',
	0x77: 'f8',
	0x78: 'f9',
	0x79: 'f10',
	0x7a: 'f11',
	0x7b: 'f12',
	0x91: 'f14',
	0x13: 'f15',
	#0x2d: 'help',
	0x2d: 'insert',
	0x2e: 'delete',
	0x24: 'home',
	0x23: 'end',
	0x21: 'page_up',
	0x22: 'page_down',
	0x25: 'left_arrow',
	0x27: 'right_arrow',
	0x26: 'up_arrow',
	0x28: 'down_arrow',
}

win_button_flags = wc.MK_LBUTTON | wc.MK_MBUTTON | wc.MK_RBUTTON
win_prev_key_state = 1 << 30

win_last_mouse_down = None
win_dbl_time = gui.GetDoubleClickTime() / 1000.0 # 0.25
win_dbl_xdist = api.GetSystemMetrics(wc.SM_CXDOUBLECLK)
win_dbl_ydist = api.GetSystemMetrics(wc.SM_CYDOUBLECLK)

def win_message_to_event(message, target = None):
	hwnd, msg, wParam, lParam, milliseconds, gpos = message
	kind, button = win_message_map[msg]
	time = milliseconds / 1000.0
	if kind == 'mouse_move' and wParam & win_button_flags <> 0:
		kind = 'mouse_drag'
	if target:
		lpos = target.global_to_local(gpos)
	else:
		lpos = gpos
	event = Event()
	event.kind = kind
	event.global_position = gpos
	event.position = lpos
	event.time = time
	event.button = button
	shift = api.GetKeyState(wc.VK_SHIFT) & 0x80 <> 0
	control = api.GetKeyState(wc.VK_CONTROL) & 0x80 <> 0
	option = api.GetKeyState(wc.VK_MENU) & 0x80 <> 0
	event.shift = event.extend_contig = shift
	event.control = event.extend_noncontig = control
	event.option = option
	vkey = None
	if kind == 'mouse_down':
		global win_last_mouse_down
		last = win_last_mouse_down
		if last and last.button == button and time - last.time <= win_dbl_time:
			x0, y0 = last.global_position
			x1, y1 = gpos
			if abs(x1 - x0) <= win_dbl_xdist and abs(y1 - y0) <= win_dbl_ydist:
				event.num_clicks = last.num_clicks + 1
		win_last_mouse_down = event
	elif kind == 'key_down' or kind == 'key_up':
		event.unichars = ui.TranslateVirtualKey(wParam)
		event.char = event.unichars.decode('ascii')
		event._keycode = wParam
		if wParam == 0x0d:
			if (lParam & 0x1000000):
				event.key = 'enter'
			else:
				event.key = 'return'
		else:
			event.key = win_special_keys.get(wParam) or event.char
		if kind == 'key_down':
			event.auto = lParam & win_prev_key_state <> 0
	return event

