#
#		Python GUI - Message handlers - Generic
#

from GUI import export

class MessageHandler(object):
	"""A MessageHandler is an object which can form part of the
	message handling hierarchy. This hierarchy is used to handle
	keyboard events, menu commands, and action messages generated
	by buttons or other components.
	
	At any given moment, one of the application's windows is the
	'target window' for messages. Within the target window, some
	component is designated as the 'target object', or just 'target'.
	
	Messages are initially delivered to the target object, and
	passed up the hierarchy using the handle() method. At each step,
	if the object has a method with the same name as the message, it
	is called with the message's arguments. Otherwise the message is
	passed on to the object determined by the next_handler() method.
	Usually this is the object's container, but need not be.

	The become_target() method is used to make a component the target
	within its window. The targeted() and untargeted() methods are
	called to notify a component when it has become or ceased to be
	the target. The is_target() method can be used to test whether a
	component is currently the target."""

	#----- Event handling -----
	
	def handle_event_here(self, event):
		"""Send an event message to this object, ignoring the event if
		there is no method to handle it."""
		#print "MessageHandler.handle_event_here:", self ###
		self.handle_here(event.kind, event)
	
	def handle_event(self, event):
		"""Send an event message up the message path until a method
		is found to handle it."""
		self.handle(event.kind, event)
	
	#----- Message handling -----
	
	def handle_here(self, message, *args):
		"""If there is a method with the same name as the message, call
		it with the given args. Otherwise, ignore the message."""
		#print "MessageHandler.handle_here:", self ###
		method = getattr(self, message, None)
		if method:
			method(*args)
	
	def handle(self, message, *args):
		"""If there is a method with the same name as the message, call
		it with the given args. Otherwise, pass the message up to the
		next handler."""
		#print "MessageHandler: handling", message, "for", self ###
		method = getattr(self, message, None)
		if method:
			#print "MessageHandler: calling method from", method.im_func.func_code.co_filename ###
			method(*args)
		else:
			#print "MessageHandler: passing to next handler" ###
			self.pass_to_next_handler(message, *args)
	
	def pass_event_to_next_handler(self, event):
		"""Pass the given event on to the next handler, if any."""
		self.pass_to_next_handler(event.kind, event)
	
	def pass_to_next_handler(self, message, *args):
		"""Pass the given message on to the next handler, if any."""
		next = self.next_handler()
		if next:
			next.handle(message, *args)

	def next_handler(self):
		"""Return the object, if any, to which messages not handled
		by this object should be passed on."""
		return None

	#----- Default handlers and callbacks -----
	
	def _setup_menus(self, m):
		self.pass_to_next_handler('_setup_menus', m)
		#print "MessageHandler._setup_menus: calling setup_menus for", self ###
		self.setup_menus(m)
	
	def setup_menus(self, m):
		"""Called before a menu is pulled down, to allow the Component to
		enable menu commands that it responds to."""
		pass
	
	_pass_key_events_to_platform = False
	
	def _default_key_event(self, event):
		#print "MessageHandler._default_key_event for", self ###
		#print "...originator =", event._originator ###
		if event._originator is self and self._pass_key_events_to_platform:
			#print "...passing to platform" ###
			event._not_handled = True
		else:
			self.pass_event_to_next_handler(event)
	
	def _default_mouse_event(self, event):
		event._not_handled = True
	
	def _event_custom_handled(self, event):
		#  Give custom event handlers of this component a chance to handle
		#  the event. If it reaches a default event method of this component,
		#  the event is not passed to the next handler and false is returned.
		#  If it is handled by an overridden method or explicitly passed to
		#  the next handler, true is returned.
		event._originator = self
		self.handle_event(event)
		return not event._not_handled
	
	def key_down(self, event):
		#print "MessageHandler.key_down for", self ###
		self._default_key_event(event)

	def key_up(self, event):
		self._default_key_event(event)

	def mouse_down(self, event):
		self._default_mouse_event(event)

	def mouse_drag(self, event):
		self._default_mouse_event(event)

	def mouse_up(self, event):
		self._default_mouse_event(event)

	def mouse_move(self, event):
		self._default_mouse_event(event)

	def mouse_enter(self, event):
		self._default_mouse_event(event)

	def mouse_leave(self, event):
		self._default_mouse_event(event)

export(MessageHandler)
