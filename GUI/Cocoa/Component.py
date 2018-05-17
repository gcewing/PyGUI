#
#   Python GUI - Components - PyObjC
#

from Foundation import NSRect, NSPoint, NSSize, NSObject
from GUI import export
from GUI import Globals, application
from GUI import Event
from GUI.GComponents import Component as GComponent

#------------------------------------------------------------------------------

Globals._ns_view_to_component = {}  # Mapping from NSView to corresponding Component

#------------------------------------------------------------------------------

class Component(GComponent):

	_has_local_coords = True
	_generic_tabbing = False
	_ns_pass_mouse_events_to_platform = False
	_ns_handle_mouse = False
	_ns_accept_first_responder = False
	_default_tab_stop = None

	def __init__(self, _ns_view, _ns_inner_view = None, _ns_responder = None,
			_ns_set_autoresizing_mask = True, **kwds):
		self._ns_view = _ns_view
		if not _ns_inner_view:
			_ns_inner_view = _ns_view
		self._ns_inner_view = _ns_inner_view
		self._ns_responder = _ns_responder or _ns_inner_view
		Globals._ns_view_to_component[_ns_view] = self
		GComponent.__init__(self, **kwds)

	def destroy(self):
		#print "Component.destroy:", self ###
		GComponent.destroy(self)
		_ns_view = self._ns_view
		if _ns_view in Globals._ns_view_to_component:
			#print "Component.destroy: removing", _ns_view, "from mapping" ###
			del Globals._ns_view_to_component[_ns_view]
		#print "Component.destroy: breaking link to", self._ns_view ###
		self._ns_view = None
		#if self._ns_inner_view: print "Component.destroy: breaking inner link to", self._ns_inner_view ###
		self._ns_inner_view = None
		self._ns_responder = None
	
	def get_bounds(self):
		(l, t), (w, h) = self._ns_view.frame()
		return (l, t, l + w, t + h)
	
	def set_bounds(self, (l, t, r, b)):
		ns = self._ns_view
		w0, h0 = ns.frame().size
		w1 = r - l
		h1 = b - t
		ns_frame = ((l, t), (w1, h1))
		old_ns_frame = ns.frame()
		ns.setFrame_(ns_frame)
		sv = ns.superview()
		if sv:
			sv.setNeedsDisplayInRect_(old_ns_frame)
			sv.setNeedsDisplayInRect_(ns_frame)
		if w0 != w1 or h0 != h1:
			self._resized((w1 - w0, h1 - h0))

	def become_target(self):
		ns_view = self._ns_view
		ns_window = ns_view.window()
		if ns_window and not self.is_target():
			self._ns_accept_first_responder = True
			ns_window.makeFirstResponder_(ns_view)
			self._ns_accept_first_responder = False

	def _ns_pass_to_platform(self, event, method_name):
		#  This method is used to direct an event intercepted by a
		#  Python subclass of an NS class to the NS method that would
		#  have handled it otherwise. It uses the '_ns_responder' attribute
		#  to find the target NS object, and the 'ns_base_class' attribute
		#  of that to find the class in which to look for the NS method.
		#  If there is no 'ns_base_class', the first base class is used.
		#print "Component._ns_pass_to_platform:", self ###
		h = self._get_ns_responder()
		b = getattr(h, 'ns_base_class', None) or h.__class__.__bases__[0]
		m = getattr(b, method_name)
		#print "...ns responder =", object.__repr__(h) ###
		#print "...ns base class =", b ###
		#print "...ns method =", m ###
		m(h, event._ns_event)
	
	def mouse_down(self, event):
		if self._ns_handle_mouse:
			self._ns_pass_to_platform(event, ns_mouse_down_methods[event.button])
	
	def mouse_drag(self, event):
		if self._ns_handle_mouse:
			self._ns_pass_to_platform(event, 'mouseDragged_')
	
	def mouse_up(self, event):
		#print "Component.mouse_up:", self ###
		if self._ns_handle_mouse:
			self._ns_pass_to_platform(event, ns_mouse_up_methods[event.button])
	
	def mouse_move(self, event):
		#self._ns_pass_to_platform(event, 'mouseMoved_')
		pass
	
	def mouse_enter(self, event):
		#self._ns_pass_to_platform(event, 'mouseEntered_')
		pass
	
	def mouse_leave(self, event):
		#self._ns_pass_to_platform(event, 'mouseExited_')
		pass
	
	def key_down(self, event):
		#print "Component.key_down:", repr(event.char), "for", self ###
		self._ns_pass_to_platform(event, 'keyDown_')
	
	def key_up(self, event):
		self._ns_pass_to_platform(event, 'keyUp_')
	
	def _get_ns_responder(self):
		return self._ns_responder

#------------------------------------------------------------------------------

ns_mouse_down_methods = {
	'left': 'mouseDown_', 'middle': 'otherMouseDown_', 'right': 'rightMouseDown_'
}

ns_mouse_up_methods = {
	'left': 'mouseUp_', 'middle': 'otherMouseUp_', 'right': 'rightMouseUp_'
}

#------------------------------------------------------------------------------

export(Component)
