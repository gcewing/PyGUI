#
#   Python GUI - Components - Gtk
#

import gtk
from gtk import gdk
from GUI import export
from GUI import Event
from GUI.Geometry import sub_pt
from GUI.GComponents import Component as GComponent

_gdk_events_of_interest = (
	gdk.POINTER_MOTION_MASK |
	gdk.BUTTON_MOTION_MASK |
	gdk.BUTTON_PRESS_MASK |
	gdk.BUTTON_RELEASE_MASK |
	gdk.KEY_PRESS_MASK |
	gdk.KEY_RELEASE_MASK |
	gdk.ENTER_NOTIFY_MASK |
	gdk.LEAVE_NOTIFY_MASK |
	0
)

_gtk_widget_to_component = {}
_gtk_last_keyval_down = None

#------------------------------------------------------------------------------

class Component(GComponent):

	_pass_key_events_to_platform = True

	def _gtk_find_component(gtk_widget):
		while gtk_widget:
			component = _gtk_widget_to_component.get(gtk_widget)
			if component:
				return component
			gtk_widget = gtk_widget.get_parent()
		return None
	
	_gtk_find_component = staticmethod(_gtk_find_component)
	
	def __init__(self, _gtk_outer, _gtk_inner = None,
			_gtk_focus = None, _gtk_input = None, **kwds):
		self._position = (0, 0)
		self._size = _gtk_outer.size_request()
		_gtk_inner = _gtk_inner or _gtk_outer
		self._gtk_outer_widget = _gtk_outer
		self._gtk_inner_widget = _gtk_inner
		self._gtk_focus_widget = _gtk_focus
		_gtk_widget_to_component[_gtk_outer] = self
		self._gtk_connect_input_events(_gtk_input or _gtk_inner)
		if _gtk_focus:
			_gtk_focus.set_property('can-focus', True)
			self._gtk_connect(_gtk_focus, 'focus-in-event', self._gtk_focus_in)
		GComponent.__init__(self, **kwds)
	
	def destroy(self):
		gtk_widget = self._gtk_outer_widget
		if gtk_widget in _gtk_widget_to_component:
			del _gtk_widget_to_component[gtk_widget]
		GComponent.destroy(self)
	
	#
	#		Properties
	#

	def set_width(self, v):
		w, h = self.size
		self.size = (v, h)

	def set_height(self, v):
		w, h = self.size
		self.size = (w, v)

	def get_position(self):
		return self._position

	def set_position(self, v):
		self._position = v
		widget = self._gtk_outer_widget
		parent = widget.get_parent()
		if parent:
			parent.move(widget, *v)
		
	def get_size(self):
		return self._size

	def set_size(self, new_size):
		w0, h0 = self._size
		w1, h1 = new_size
		self._gtk_outer_widget.set_size_request(max(int(w1), 1), max(int(h1), 1))
		self._size = new_size
		if w0 != w1 or h0 != h1:
			self._resized((w1 - w0, h1 - h0))
	
	def get_bounds(self):
		x, y = self._position
		w, h = self.size
		return (x, y, x + w, y + h)

	def set_bounds(self, (l, t, r, b)):
		self.position = (l, t)
		self.size = (r - l, b - t)

#	def get_visible(self):
#		return self._gtk_outer_widget.get_property('visible')
#	
#	def set_visible(self, v):
#		self._gtk_outer_widget.set_property('visible', v)
	
	#
	#   Message dispatching
	#

	def become_target(self):
		gtk_focus = self._gtk_focus_widget
		if gtk_focus:
			gtk_focus.grab_focus()
		else:
			raise ValueError("%r cannot be targeted" % self)

#	def current_target(self):
#		"""Find the current target object within the Window containing
#		this component. If the component is not contained in a Window,
#		the result is undefined."""
#		target = _gtk_find_component(self._gtk_outer_widget.get_focus())
#		if not target:
#			target = self.window
#		return target

	def is_target(self):
		"""Return true if this is the current target within the containing
		Window. If the component is not contained in a Window, the result
		is undefined."""
		gtk_focus = self._gtk_focus_widget
		if gtk_focus:
			return gtk_focus.get_property('has-focus')
		else:
			return False
	
	#
	#   Internal
	#
	
	def _gtk_connect(self, gtk_widget, signal, handler):
		def catch(widget, *args):
			try:
				handler(*args)
			except:
				_gtk_exception_in_signal_handler()
		gtk_widget.connect(signal, lambda widget, *args: handler(*args))

	def _gtk_connect_after(self, gtk_widget, signal, handler):
		def catch(widget, *args):
			try:
				handler(*args)
			except:
				_gtk_exception_in_signal_handler()
		gtk_widget.connect_after(signal, lambda widget, *args: handler(*args))

	def _gtk_focus_in(self, gtk_event):
		window = self.window
		if window:
			old_target = window._target
			window._target = self
			if old_target and old_target is not self:
				old_target.untargeted()
				self.targeted()
# 				old_target._untargeted()
# 				self._targeted()

# 	def _targeted(self):
# 		pass
# 	
# 	def _untargeted(self):
# 		pass
	
	def _gtk_connect_input_events(self, gtk_widget):
		self._last_mouse_down_time = 0
		self._click_count = 0
		gtk_widget.add_events(_gdk_events_of_interest)
		self._gtk_connect(gtk_widget, 'button-press-event',
			self._gtk_button_press_event_signal)
		self._gtk_connect(gtk_widget, 'motion-notify-event',
			self._gtk_motion_notify_event_signal)
		self._gtk_connect(gtk_widget, 'button-release-event',
			self._gtk_button_release_event_signal)
		self._gtk_connect(gtk_widget, 'enter-notify-event',
			self._gtk_enter_leave_event_signal)
		self._gtk_connect(gtk_widget, 'leave-notify-event',
			self._gtk_enter_leave_event_signal)
		self._gtk_connect(gtk_widget, 'key-press-event',
			self._handle_gtk_key_event)
		self._gtk_connect(gtk_widget, 'key-release-event',
			self._handle_gtk_key_event)

	def _gtk_button_press_event_signal(self, gtk_event):
		if gtk_event.type == gdk.BUTTON_PRESS: # don't want 2BUTTON or 3BUTTON
			event = Event._from_gtk_mouse_event(gtk_event)
			last_time = self._last_mouse_down_time
			this_time = event.time
			num_clicks = self._click_count
			if this_time - last_time <= 0.25:
				num_clicks += 1
			else:
				num_clicks = 1
			event.num_clicks = num_clicks
			self._click_count = num_clicks
			self._last_mouse_down_time = this_time
			#print "Component._gtk_button_press_event_signal:" ###
			#print event ###
			return self._event_custom_handled(event)
	
	def _gtk_motion_notify_event_signal(self, gtk_event):
		event = Event._from_gtk_mouse_event(gtk_event)
		self._mouse_event = event
		return self._event_custom_handled(event)

	def _gtk_button_release_event_signal(self, gtk_event):
		event = Event._from_gtk_mouse_event(gtk_event)
		self._mouse_event = event
		return self._event_custom_handled(event)

	def _gtk_enter_leave_event_signal(self, gtk_event):
		#print "Component._gtk_enter_leave_event_signal:" ###
		event = Event._from_gtk_mouse_event(gtk_event)
		return self._event_custom_handled(event)

	def _handle_gtk_key_event(self, gtk_event):
		"""Convert a Gtk key-press or key-release event into an Event
		object and pass it up the message path."""
		#print "Component._handle_gtk_key_event for", self ###
		global _gtk_last_keyval_down
		if Event._gtk_key_event_of_interest(gtk_event):
			event = Event._from_gtk_key_event(gtk_event)
			if event.kind == 'key_down':
				this_keyval = gtk_event.keyval
				if _gtk_last_keyval_down == this_keyval:
					event.auto = 1
				_gtk_last_keyval_down = this_keyval
			else:
				_gtk_last_keyval_down = None
			#if event.kind == 'key_down': ###
			#	print event ###
			return self._event_custom_handled(event)

#------------------------------------------------------------------------------

def _gtk_exception_in_signal_handler():
	print >>sys.stderr, "---------- Exception in gtk signal handler ----------"
	traceback.print_exc()

export(Component)
