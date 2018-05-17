#
#		Python GUI - Events - Gtk
#

from gtk import gdk
from GUI import export
from GUI.GEvents import Event as GEvent

_gdk_button_mask = (
	gdk.BUTTON1_MASK |
	gdk.BUTTON2_MASK |
	gdk.BUTTON3_MASK |
	gdk.BUTTON4_MASK |
	gdk.BUTTON5_MASK
)

_gdk_event_type_to_kind = {
	gdk.BUTTON_PRESS:     'mouse_down',
	gdk._2BUTTON_PRESS:   'mouse_down',
	gdk._3BUTTON_PRESS:   'mouse_down',
	gdk.MOTION_NOTIFY:    'mouse_move',
	gdk.BUTTON_RELEASE:   'mouse_up',
	gdk.KEY_PRESS:        'key_down',
	gdk.KEY_RELEASE:      'key_up',
	gdk.ENTER_NOTIFY:     'mouse_enter',
	gdk.LEAVE_NOTIFY:     'mouse_leave',
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
	0xFF0D: 'return',
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

	def _gtk_key_event_of_interest(gtk_event):
		keyval = gtk_event.keyval
		return (keyval <= 0xFF 
			or 0xFF00 <= keyval <= 0xFF1F
			or 0xFF80 <= keyval <= 0xFFBD
			or keyval == 0xFE20 # shift-tab
			or keyval == 0xFFFF
			or keyval in _gdk_keyval_to_keyname)
	
	_gtk_key_event_of_interest = staticmethod(_gtk_key_event_of_interest)

	def _from_gtk_key_event(cls, gtk_event):
		event = cls.__new__(cls)
		event._set_from_gtk_event(gtk_event)
		keyval = gtk_event.keyval
		event._keycode = keyval
		#print "Event._from_gtk_key_event: keyval = 0x%04X" % keyval ###
		key = _gdk_keyval_to_keyname.get(keyval, "")
		if keyval == 0xFFFF: # GDK_Delete
			char = "\x7F"
		elif keyval == 0xFF8D:
			char = "\r"
		elif keyval == 0xFE20: # shift-tab
			char = "\t"
		elif keyval <= 0xFF1F:
			if event.control:
				char = chr(keyval & 0x1F)
			else:
				char = chr(keyval & 0x7F)
		else:
			char = ""
		if not key and "\x20" <= char <= "\x7e":
			key = char
		event.char = char
		event.key = key
		event.unichars = unicode(char)
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
		state = gtk_event.state
		if typ == gdk.MOTION_NOTIFY and state & _gdk_button_mask:
			self.kind = 'mouse_drag'
		else:
			self.kind = _gdk_event_type_to_kind[gtk_event.type]
		self.time = gtk_event.time / 1000.0
		self.shift = self.extend_contig = (state & gdk.SHIFT_MASK) <> 0
		self.control = self.extend_noncontig = (state & gdk.CONTROL_MASK) <> 0
		self.option = self.mod1 = (state & gdk.MOD1_MASK) <> 0

	def _platform_modifiers_str(self):
		return " mod1:%s" % (self.mod1)

export(Event)
