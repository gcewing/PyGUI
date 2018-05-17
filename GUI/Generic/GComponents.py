#
#		Python GUI - Components - Generic
#

import os
from GUI.Properties import Properties, overridable_property
from GUI import MessageHandler
from GUI.Geometry import add_pt, sub_pt, rect_size, rect_sized, rect_topleft
from GUI import application

_user_tab_stop = os.environ.get("PYGUI_KEYBOARD_NAVIGATION") or None
#  Allow "False", "True", "0", "1"
if _user_tab_stop is not None:
	_user_tab_stop = _user_tab_stop.strip().capitalize()
	try:
		_user_tab_stop = {"False": False, "True": True}[_user_tab_stop]
	except KeyError:
		try:
			_user_tab_stop = int(_user_tab_stop)
		except ValueError:
			sys.stderr.write("PYGUI_KEYBOARD_NAVIGATION: Unrecognized value %r"
				% _user_tab_stop)
			_user_tab_stop = None

class Component(Properties, MessageHandler):
	"""Component is an abstract class representing a user
	interface component."""

	left = overridable_property('left', "Position of left edge relative to container.")
	top = overridable_property('top', "Position of top edge relative to container.")
	right = overridable_property('right', "Position of right edge relative to container.")
	bottom = overridable_property('bottom', "Position of bottom edge relative to container.")
	
	x = overridable_property('x', "Horizontal position relative to container.")
	y = overridable_property('y', "Vertical position relative to container.")
	width = overridable_property('width')
	height = overridable_property('height')
	
	position = overridable_property('position', "Position relative to container.")
	size = overridable_property('size')
	
	bounds = overridable_property('bounds', "Bounding rectangle in container's coordinates.")
	
	container = overridable_property('container',
		"Container which contains this Component. Setting this property has the "
		"effect of removing the component from its previous container, if any, "
		"and adding it to the new one, if any.")
	
#	visible = overridable_property('visible',
#		"Whether the component is currently shown.")	

	tab_stop = overridable_property('tab_stop',
		"Whether tab key can navigate into this control.")
	
	anchor = overridable_property('anchor', "A string of 'ltrb' controlling behaviour when container is resized.")
	
	border = overridable_property('border', "True if the component should have a border.")

	_is_scrollable = False  #  Overridden by scrollable subclasses
	_generic_tabbing = True # Whether to use generic tab navigation code
	_default_tab_stop = False
	_user_tab_stop_override = False # Whether user preference overrides _default_tab_stop
	_tab_stop = None

	#
	#   Class variables defined by implementations:
	#
	#  _has_local_coords   bool   True if component has a local coordinate system
	#

	_container = None
	_border = False
	hmove = 0
	vmove = 0
	hstretch = 0
	vstretch = 0

	def __init__(self, tab_stop = None, **kwds):
		Properties.__init__(self, **kwds)
		if tab_stop is None:
			tab_stop = self._get_default_tab_stop()
		self.tab_stop = tab_stop

	def destroy(self):
		self.container = None

	#
	#		Geometry properties
	#
	#   Default implementations of position and size properties
	#   in terms of the bounds property. A minimal implementation
	#   need only implement get_bounds and set_bounds.
	#
	#   It is the implementation's responsibility to call _resized()
	#   whenever the size of the component changes, either by
	#   explicit assignment to geometry properties or by the user
	#   resizing the containing window. It should not be called if
	#   setting a geometry property does not cause the size to change.
	#

	def get_left(self):
		return self.position[0]

	def set_left(self, v):
		l, t, r, b = self.bounds
		self.bounds = (v, t, r, b)

	def get_top(self):
		return self.bounds[1]

	def set_top(self, v):
		l, t, r, b = self.bounds
		self.bounds = (l, v, r, b)

	def get_right(self):
		return self.bounds[2]

	def set_right(self, v):
		l, t, r, b = self.bounds
		self.bounds = (l, t, v, b)

	def get_bottom(self):
		return self.bounds[3]
	
	def set_bottom(self, v):
		l, t, r, b = self.bounds
		self.bounds = (l, t, r, v)

	def get_x(self):
		return self.bounds[0]

	def set_x(self, v):
		l, t, r, b = self.bounds
		self.bounds = (v, t, v + r - l, b)

	def get_y(self):
		return self.bounds[1]

	def set_y(self, v):
		l, t, r, b = self.bounds
		self.bounds = (l, v, r, v + b - t)
	
	def get_position(self):
		l, t, r, b = self.bounds
		return (l, t)
	
	def set_position(self, (x, y)):
		l, t, r, b = self.bounds
		self.bounds = (x, y, x + r - l, y + b - t)

	def get_width(self):
		l, t, r, b = self.bounds
		return r - l
	
	def set_width(self, v):
		l, t, r, b = self.bounds
		self.bounds = (l, t, l + v, b)

	def get_height(self):
		l, t, r, b = self.bounds
		return b - t
	
	def set_height(self, v):
		l, t, r, b = self.bounds
		self.bounds = (l, t, r, t + v)
	
	def get_size(self):
		l, t, r, b = self.bounds
		return (r - l, b - t)
	
	def set_size(self, (w, h)):
		l, t, r, b = self.bounds
		self.bounds = (l, t, l + w, t + h)
	
	#
	#  Container management
	#
	
	def get_container(self):
		return self._container
	 
	def set_container(self, new_container):
		if self._container != new_container:
			self._change_container(new_container)
	
	def _change_container(self, new_container):
		old_container = self._container
		if old_container:
			self._container = None
			old_container._remove(self)
		if new_container:
			self._container = new_container
			new_container._add(self)
	
	#
	#   Message dispatching
	#

	def become_target(self):
		"""Arrange for this object to be the first to handle messages
		dispatched to the containing Window. If the component is not
		contained in a Window, the effect is undefined."""
		raise NotImplementedError

	def is_target(self):
		"""Return true if this is the current target within the containing
		Window. If the component is not contained in a Window, the result
		is undefined."""
		return self.window and self.window.target is self
	
	#
	#		Message handling
	#
	
	def next_handler(self):
		return self._container

	#
	#		Visibility control
	#

#	def show(self):
#		"""Make the Component visible (provided its container is visible)."""
#		self.visible = 1
#
#	def hide(self):
#		"""Make the Component invisible."""
#		self.visible = 0

	#
	#   Border
	#
	
	def get_border(self):
		return self._border
	
	def set_border(self, x):
		self._border = x
	
	#
	#		Resizing
	#
	
	def get_anchor(self):
		if self.hmove:
			s1 = 'r'
		elif self.hstretch:
			s1 = 'lr'
		else:
			s1 = 'l'
		if self.vmove:
			s2 = 'b'
		elif self.vstretch:
			s2 = 'tb'
		else:
			s2 = 't'
		return s1 + s2
	
	def set_anchor(self, s):
		if 'r' in s:
			if 'l' in s:
				self.hstretch = True
				self.hmove = False
			else:
				self.hstretch = False
				self.hmove = True
		else:
			self.hstretch = False
			self.hmove = False
		if 'b' in s:
			if 't' in s:
				self.vstretch = True
				self.vmove = False
			else:
				self.vstretch = False
				self.vmove = True
		else:
			self.vstretch = False
			self.vmove = False
	
	def get_auto_layout(self):
		return self._auto_layout
	
	def set_auto_layout(self, x):
		self._auto_layout = x
	
	def _resized(self, delta):
		#  Called whenever the size of the component changes for
		#  any reason.
		pass

	def container_resized(self, delta):
		"""Called whenever the component's container changes size and the
		container's auto_layout property is true. The default implementation
		repositions and resizes this component according to its resizing
		options."""
		dw, dh = delta
		left, top, right, bottom = self.bounds
		if self.hmove:
			left += dw
			right += dw
		elif self.hstretch:
			right += dw
		if self.vmove:
			top += dh
			bottom += dh
		elif self.vstretch:
			bottom += dh
		self.bounds = (left, top, right, bottom)
	
	#
	#		Update region maintenance
	#

	def invalidate(self):
		"""Mark the whole Component as needing to be redrawn."""
		self.invalidate_rect(self.viewed_rect())
	
#	def invalidate_rect(self, r):
#		print "GComponent.invalidate_rect:", self, r ###
#		container = self._container
#		if container:
#			container.invalidate_rect(r)
	
#	def _invalidate_in_container(self):
#		container = self._container
#		if container:
#			container._invalidate_subcomponent(self)

	#
	#		Coordinate transformation
	#

	def local_to_global(self, p):
		p = self.local_to_container(p)
		parent = self._container
		if parent:
			return parent.local_to_global(p)
		else:
			return p

	def global_to_local(self, p):
		parent = self._container
		if parent:
			p = parent.global_to_local(p)
		return self.container_to_local(p)
	
	def local_to_container(self, p):
		if self._has_local_coords:
			return add_pt(p, self.local_to_container_offset())
		else:
			return p
	
	def container_to_local(self, p):
		if self._has_local_coords:
			return sub_pt(p, self.local_to_container_offset())
		else:
			return p

	def local_to_container_offset(self):
		if self._has_local_coords:
			return self.position
		else:
			return (0, 0)
	
	def transform_from(self, other, p):
		return transform_coords(other, self, p)
	
	def transform_to(self, other, p):
		return transform_coords(self, other, p)

	#
	#   Placement specification support
	#
	
	def __add__(self, offset):
		return (self, offset)
	
	def __sub__(self, offset):
		return (self, -offset)
	
	#
	#   Tabbing
	#
	
	def get_tab_stop(self):
		return self._tab_stop
	
	def set_tab_stop(self, x):
		if self._tab_stop <> x:
			self._tab_stop = x
			self._invalidate_tab_chain()

	def _get_default_tab_stop(self):
		if self._user_tab_stop_override:
			result = _user_tab_stop
		else:
			result = None
		if result is None:
			result = self._default_tab_stop
		return result

	def _tab_out(self):
		pass
	
	def _tab_in(self):
		self.become_target()
	
	def _build_tab_chain(self, chain):
		if self._tab_stop:
			chain.append(self)
	
	def _invalidate_tab_chain(self):
		window = self.window
		if window:
			window._invalidate_tab_chain()
	
	def _is_targetable(self):
		return True

	#
	#		Other
	#
	
	def targeted(self):
		"""Called when the component becomes the target within its Window."""
		pass

	def untargeted(self):
		"""Called when the component ceases to be the target within its Window."""
		pass

	window = overridable_property('window', """The Window ultimately containing
		this Component, or None.""")
	
	def get_window(self):
		container = self._container
		if container:
			return container.window
		else:
			return None

	def reset_blink(self):
		application().reset_blink()
	
	def viewed_rect(self):
		"""Returns the rectangle in local coordinates that is
		currently visible within the component."""
		if self._has_local_coords:
			width, height = self.size
			return (0, 0, width, height)
		else:
			return self.bounds
	
	def broadcast(self, message, *args):
		"""Traverse the component hierarchy, calling each component's handler for
		the given message, if any."""
		method = getattr(self, message, None)
		if method:
			method(*args)

	def _dispatch_mouse_event(self, event):
		self._handle_mouse_event(event)
	
	def _handle_mouse_event(self, event):
		self.handle(event.kind, event)


def transform_coords(from_component, to_component, p):
	if from_component:
		g = from_component.local_to_global(p)
	else:
		g = p
	if to_component:
		return to_component.global_to_local(g)
	else:
		return g
