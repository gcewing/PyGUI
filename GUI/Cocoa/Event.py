#
#		Python GUI - Events - PyObjC version
#

import AppKit
from AppKit import NSEvent, \
	NSShiftKeyMask, NSControlKeyMask, NSCommandKeyMask, NSAlternateKeyMask
from GUI import export
from GUI import Globals
from GUI.GEvents import Event as GEvent

_ns_event_type_to_kind = {
	AppKit.NSLeftMouseDown: 'mouse_down',
	AppKit.NSLeftMouseUp: 'mouse_up',
	AppKit.NSRightMouseDown: 'mouse_down',
	AppKit.NSRightMouseUp: 'mouse_up',
	AppKit.NSOtherMouseDown: 'mouse_down',
	AppKit.NSOtherMouseUp: 'mouse_up',
	AppKit.NSMouseMoved: 'mouse_move',
	AppKit.NSLeftMouseDragged: 'mouse_drag',
	AppKit.NSRightMouseDragged: 'mouse_drag',
	AppKit.NSOtherMouseDragged: 'mouse_drag',
	AppKit.NSMouseEntered: 'mouse_enter',
	AppKit.NSMouseExited: 'mouse_leave',
	AppKit.NSKeyDown: 'key_down',
	AppKit.NSKeyUp: 'key_up',
	AppKit.NSFlagsChanged: 'flags_changed',
	AppKit.NSAppKitDefined: 'app_kit_defined',
	AppKit.NSSystemDefined: 'system_defined',
	AppKit.NSApplicationDefined: 'application_defined',
	AppKit.NSPeriodic: 'periodic',
	AppKit.NSCursorUpdate: 'cursor_update',
}

_ns_event_type_to_button = {
	AppKit.NSLeftMouseDown: 'left',
	AppKit.NSLeftMouseUp: 'left',
	AppKit.NSRightMouseDown: 'right',
	AppKit.NSRightMouseUp: 'right',
	AppKit.NSOtherMouseDown: 'middle',
	AppKit.NSOtherMouseUp: 'middle',
	AppKit.NSLeftMouseDragged: 'left',
	AppKit.NSRightMouseDragged: 'right',
	AppKit.NSOtherMouseDragged: 'middle',
}

_ns_keycode_to_keyname = {
	AppKit.NSUpArrowFunctionKey: 'up_arrow',
	AppKit.NSDownArrowFunctionKey: 'down_arrow',
	AppKit.NSLeftArrowFunctionKey: 'left_arrow',
	AppKit.NSRightArrowFunctionKey: 'right_arrow',
	AppKit.NSF1FunctionKey: 'f1',
	AppKit.NSF2FunctionKey: 'f2',
	AppKit.NSF3FunctionKey: 'f3',
	AppKit.NSF4FunctionKey: 'f4',
	AppKit.NSF5FunctionKey: 'f5',
	AppKit.NSF6FunctionKey: 'f6',
	AppKit.NSF7FunctionKey: 'f7',
	AppKit.NSF8FunctionKey: 'f8',
	AppKit.NSF9FunctionKey: 'f9',
	AppKit.NSF10FunctionKey: 'f10', 
	AppKit.NSF11FunctionKey: 'f11',
	AppKit.NSF12FunctionKey: 'f12',
	AppKit.NSF13FunctionKey: 'f13',
	AppKit.NSF14FunctionKey: 'f14',
	AppKit.NSF15FunctionKey : 'f15',
	AppKit.NSDeleteFunctionKey: 'delete',
	AppKit.NSHomeFunctionKey: 'home',
	AppKit.NSEndFunctionKey: 'end',
	AppKit.NSPageUpFunctionKey: 'page_up',
	AppKit.NSPageDownFunctionKey: 'page_down',
	AppKit.NSClearLineFunctionKey: 'clear',
	#AppKit.NSHelpFunctionKey: 'help',
	AppKit.NSHelpFunctionKey: 'insert',
	"\r": 'return',
	"\x03": 'enter',
}

_mouse_events = [
	'mouse_down', 'mouse_drag', 'mouse_up',
	'mouse_move', 'mouse_enter', 'mouse_exit'
]

_key_events = [
	'key_down', 'key_up'
]

_ns_screen_height = None

class Event(GEvent):
	"""Platform-dependent modifiers (boolean):
		command            The Macintosh Command key.
		option             The Macintosh Option key.
	"""

	global_position = (0, 0)
	position = (0, 0)
	button = ''
	num_clicks = 0
	char = ""
	unichars = ""
	key = ''
	auto = False
	delta = (0, 0)

	def __init__(self, ns_event):
		self._ns_event = ns_event
		_ns_type = ns_event.type()
		kind = _ns_event_type_to_kind[_ns_type]
		self.kind = kind
		self.time = ns_event.timestamp()
		ns_window = ns_event.window()
		is_mouse_event = kind in _mouse_events
		if is_mouse_event:
			ns_win_pos = ns_event.locationInWindow()
			x, y = ns_window.convertBaseToScreen_(ns_win_pos)
		else:
			ns_last_mouse = Globals.ns_last_mouse_moved_event
			if ns_last_mouse:
				ns_window = ns_last_mouse.window()
				if ns_window:
					ns_win_pos = ns_last_mouse.locationInWindow()
					x, y = ns_window.convertBaseToScreen_(ns_win_pos)
				else:
					x, y = ns_last_mouse.locationInWindow()
			else:
				x, y = NSEvent.mouseLocation()
		h = Globals.ns_screen_height
		self.global_position = (x, h - y)
		if is_mouse_event:
			self.button = _ns_event_type_to_button.get(_ns_type, '')
			if kind == 'mouse_down':
				self.num_clicks = ns_event.clickCount()
			self.delta = (ns_event.deltaX(), ns_event.deltaY())
		ns_flags = ns_event.modifierFlags()
		self.shift = self.extend_contig = (ns_flags & NSShiftKeyMask) <> 0
		self.control = (ns_flags & NSControlKeyMask) <> 0
		self.command = self.extend_noncontig = (ns_flags & NSCommandKeyMask) <> 0
		self.option = (ns_flags & NSAlternateKeyMask) <> 0
		if kind in _key_events:
			self.auto = ns_event.isARepeat()
			ns_chars = ns_event.characters()
			#print "Event.__init__: ns_chars =", repr(ns_chars) ###
			self.unichars = ns_chars
			if len(ns_chars) == 1:
				if ns_chars == "\x19" and ns_event.keyCode() == 48:
					self.char = "\t"
				elif ns_chars == "\x7f":
					self.char = "\x08"
				elif ns_chars <= "\x7e":
					self.char = str(ns_chars)
				#else:
				#	self.char = ns_chars
			ns_unmod = ns_event.charactersIgnoringModifiers()
			key = _ns_keycode_to_keyname.get(ns_chars, '')
			if not key and u"\x20" <= ns_unmod <= u"\x7e":
				key = str(ns_unmod)
			self.key = key
			if key == 'enter':
				self.char = "\r"
			elif key == 'delete':
				self.char = "\x7f"

	def _platform_modifiers_str(self):
		return " command:%s option:%s" % (self.command, self.option)

export(Event)
