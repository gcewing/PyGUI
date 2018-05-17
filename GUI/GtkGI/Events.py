#
#		Python GUI - Events - Gtk
#

from gi.repository import Gdk
from GUI.GEvents import Event as GEvent

MOTION_NOTIFY = Gdk.EventType.MOTION_NOTIFY

SHIFT_MASK = Gdk.ModifierType.SHIFT_MASK
CONTROL_MASK = Gdk.ModifierType.CONTROL_MASK
MOD1_MASK = Gdk.ModifierType.MOD1_MASK
MOD2_MASK = Gdk.ModifierType.MOD2_MASK
MOD3_MASK = Gdk.ModifierType.MOD3_MASK
MOD4_MASK = Gdk.ModifierType.MOD4_MASK
MOD5_MASK = Gdk.ModifierType.MOD5_MASK
BIT13_MASK = 0x2000
SUPER_MASK = Gdk.ModifierType.SUPER_MASK
HYPER_MASK = Gdk.ModifierType.HYPER_MASK
META_MASK = Gdk.ModifierType.META_MASK

_gdk_button_mask = (
	Gdk.ModifierType.BUTTON1_MASK |
	Gdk.ModifierType.BUTTON2_MASK |
	Gdk.ModifierType.BUTTON3_MASK |
	Gdk.ModifierType.BUTTON4_MASK |
	Gdk.ModifierType.BUTTON5_MASK
)

_gdk_event_type_to_kind = {
	Gdk.EventType.BUTTON_PRESS:     'mouse_down',
	Gdk.EventType._2BUTTON_PRESS:   'mouse_down',
	Gdk.EventType._3BUTTON_PRESS:   'mouse_down',
	Gdk.EventType.MOTION_NOTIFY:    'mouse_move',
	Gdk.EventType.BUTTON_RELEASE:   'mouse_up',
	Gdk.EventType.KEY_PRESS:        'key_down',
	Gdk.EventType.KEY_RELEASE:      'key_up',
	Gdk.EventType.ENTER_NOTIFY:     'mouse_enter',
	Gdk.EventType.LEAVE_NOTIFY:     'mouse_leave',
}

_gtk_button_to_button = {
	1: 'left',
	2: 'middle',
	3: 'right',
	4: 'fourth',
	5: 'fifth',
}

_gdk_keyval_to_keyname = {
	0xFF50: 'home',
	0xFF51: 'left_arrow',
	0xFF52: 'up_arrow',
	0xFF53: 'right_arrow',
	0xFF54: 'down_arrow',
	0xFF55: 'page_up',
	0xFF56: 'page_down',
	0xFF57: 'end',
	#0xFF6A: 'help',
	0xFF6A: 'insert',
	0xFF8D: 'enter',
	0xFFBE: 'f1',
	0xFFBF: 'f2',
	0xFFC0: 'f3',
	0xFFC1: 'f4',
	0xFFC2: 'f5',
	0xFFC3: 'f6',
	0xFFC4: 'f7',
	0xFFC5: 'f8',
	0xFFC6: 'f9',
	0xFFC7: 'f10',
	0xFFC8: 'f11',
	0xFFC9: 'f12',
	0xFFCA: 'f13',
	0xFFCB: 'f14',
	0xFFCC: 'f15',
	0xFFFF: 'delete',
}

def _gtk_key_event_of_interest(gtk_event):
	keyval = gtk_event.keyval
	return (keyval <= 0xFF 
		or 0xFF00 <= keyval <= 0xFF1F
		or 0xFF80 <= keyval <= 0xFFBD
		or keyval == 0xFE20 # shift-tab
		or keyval == 0xFFFF
		or keyval in _gdk_keyval_to_keyname)

class Event(GEvent):
	"""Platform-dependent modifiers (boolean):
		mod1            The X11 MOD1 key.
	"""
	
	button = None
	position = None
	global_position = None
	num_clicks = 0
	char = None
	key = None
	auto = 0

	def _from_gtk_key_event(cls, gtk_event):
		event = cls.__new__(cls)
		event._set_from_gtk_event(gtk_event)
		keyval = gtk_event.keyval
		#print "Event._from_gtk_key_event: keyval = 0x%04X" % keyval ###
		event.key = _gdk_keyval_to_keyname.get(keyval, "")
		if keyval == 0xFFFF: # GDK_Delete
			event.char = chr(0x7F)
		elif keyval == 0xFF8D:
			event.char = "\r"
		elif keyval == 0xFE20: # shift-tab
			event.char = "\t"
		elif keyval <= 0xFF1F:
			if event.control:
				event.char = chr(keyval & 0x1F)
			else:
				event.char = chr(keyval & 0x7F)
		else:
			event.char = ""
		return event

	_from_gtk_key_event = classmethod(_from_gtk_key_event)
	
	def _from_gtk_mouse_event(cls, gtk_event):
		event = cls.__new__(cls)
		event._set_from_gtk_event(gtk_event)
		if event.kind in ('mouse_down', 'mouse_up'):
			event.button = _gtk_button_to_button[gtk_event.button]
		event.position = (gtk_event.x, gtk_event.y)
		event.global_position = (gtk_event.x_root, gtk_event.y_root)
		return event
	
	_from_gtk_mouse_event = classmethod(_from_gtk_mouse_event)
	
	def _set_from_gtk_event(self, gtk_event):
		typ = gtk_event.type
		state = gtk_event.get_state()
		#print "Event: gtk state = 0x%x" % state ###
		if typ == MOTION_NOTIFY and state & _gdk_button_mask:
			self.kind = 'mouse_drag'
		else:
			self.kind = _gdk_event_type_to_kind[gtk_event.type]
		self.time = gtk_event.time / 1000.0
		self.shift = self.extend_contig = (state & SHIFT_MASK) <> 0
		self.control = self.extend_noncontig = (state & CONTROL_MASK) <> 0
		self.mod1 = (state & MOD1_MASK) <> 0
		self.mod2 = (state & MOD2_MASK) <> 0
		self.mod3 = (state & MOD3_MASK) <> 0
		self.mod4 = (state & MOD4_MASK) <> 0
		self.mod5 = (state & MOD5_MASK) <> 0
		self.super = (state & SUPER_MASK) <> 0
		self.hyper = (state & HYPER_MASK) <> 0
		self.meta = (state & META_MASK) <> 0
		bit13 = (state & BIT13_MASK) <> 0 # X server on MacOSX maps Option to this
		self.option = self.mod1 or bit13

	def _platform_modifiers_str(self):
		return " mod1:%s mod2:%s mod3:%s mod4:%s mod5:%s super:%s hyper:%s meta:%s" % (
			self.mod1, self.mod2, self.mod3, self.mod4, self.mod5,
			self.super, self.hyper, self.meta)
