#
#		Python GUI - Events - Generic
#

class Event(object):

	"""An input event.
	
	Attributes:

		kind							 Type of event. One of 'mouse_down', 'mouse_up', 'key_down',
											 'key_up'.

		global_position		 Position of mouse in screen coordinates at the time of the event.

		position					 For mouse events, position in local coordinates of the View that
											 was the target of this event. Undefined for other event types.

		time							 Time of event, in platform-dependent units.

    button             Button identifier for mouse down/up events.

		num_clicks				 Number of consecutive clicks within double-click time.

		char							 For key events, an ASCII character. Undefined for other event types.
		
		key                For non-printing keys, a value identifying the key. Undefined for other event types.

		auto               True if key-down event is an autorepeat (not supported on all platforms).

	Platform-independent modifiers (boolean):

		shift              The Shift key.
		control            The Control key.
		option             The additional modifier key.
		extend_contig      The contiguous selection extension modifier key.
		extend_noncontig   The noncontiguous selection extension modifier key.
	"""
	
	kind = None
	global_position = None
	position = None
	time = None
	button = None
	num_clicks = 0
	char = None
	key = None
	auto = False
	shift = False
	control = False
	option = False
	extend_contig = False
	extend_noncontig = False
	delta = (0, 0)
	_keycode = 0 # Platform-dependent key code
	_originator = None # Component to which originally delivered by platform
	_not_handled = False # Reached default event method of originating component

	def position_in(self, view):
		"""Return the position of this event in the coordinate system
		of the specified view."""
		return view.global_to_local(self.global_position)	

	def __str__(self):
		return "<GUI.Event: %s global:%s local:%s time:%s clicks:%s char:%r" \
			" key:%s shift:%s control:%s option:%s extend_contig:%s" \
			" extend_noncontig:%s auto:%s%s>" \
			% (self.kind, self.global_position, self.position, self.time,
				self.num_clicks, self.char, self.key, self.shift, self.control,
				self.option, self.extend_contig, self.extend_noncontig, self.auto,
				self._platform_modifiers_str())
