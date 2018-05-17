#
#		Python GUI - Containers - Generic
#

try:
	maketrans = str.maketrans
except AttributeError:
	from string import maketrans
from GUI.Properties import overridable_property
from GUI.Exceptions import ArgumentError
from GUI.Geometry import pt_in_rect
from GUI import Component

anchor_to_sticky = maketrans("ltrb", "wnes")

class Container(Component):
	"""A Container is a Component that can contain other Components.
	The sub-components are clipped to the boundary of their container."""

	contents = overridable_property('contents',
		"List of subcomponents. Do not modify directly.")

	content_width = overridable_property('content_width', "Width of the content area.")
	content_height = overridable_property('content_height', "Height of the content area.")
	content_size = overridable_property('content_size', "Size of the content area.")
	
	auto_layout = overridable_property('auto_layout',
		"Automatically adjust layout of subcomponents when resized.")
	
	_auto_layout = True

	#  _contents   [Component]

	def __init__(self, **kw):
		self._contents = []
		Component.__init__(self, **kw)

	def destroy(self):
		"""Destroy this Container and all of its contents."""
		contents = self._contents
		while contents:
			comp = contents[-1]
			comp.destroy()
			assert not contents or contents[-1] is not comp, \
				"%r failed to remove itself from container on destruction" % comp
		Component.destroy(self)

	#
	#   Content area
	#
	
	def get_content_width(self):
		return self.content_size[0]
	
	def set_content_width(self, w):
		self.content_size = w, self.content_height

	def get_content_height(self):
		return self.content_size[1]

	def set_content_height(self, h):
		self.content_size = self.content_width, h
	
	get_content_size = Component.get_size
	set_content_size = Component.set_size

	#
	#		Subcomponent Management
	#
	
	def get_contents(self):
		return self._contents

	def add(self, comp):
		"""Add the given Component as a subcomponent."""
		if comp:
			if isinstance(comp, Component):
				comp.container = self
			else:
				for item in comp:
					self.add(item)

	def remove(self, comp):
		"""Remove subcomponent, if present."""
		if isinstance(comp, Component):
			if comp in self._contents:
				comp.container = None
		else:
			for item in comp:
				self.remove(item)
	
	def _add(self, comp):
		# Called by comp.set_container() to implement subcomponent addition.
		self._contents.append(comp)
		self._invalidate_tab_chain()
		self.added(comp)
	
	def _remove(self, comp):
		# Called by comp.set_container() to implement subcomponent removal.
		self._contents.remove(comp)
		self._invalidate_tab_chain()
		self.removed(comp)
	
	def added(self, comp):
		"""Called after a subcomponent has been added."""
		pass
	
	def removed(self, comp):
		"""Called after a subcomponent has been removed."""
		pass
	
	#
	#   The infamous 'place' method and friends.
	#
	
	_place_default_spacing = 8
	
	def place(self, item, 
			left = None, right = None, top = None, bottom = None,
			sticky = 'nw', scrolling = '', border = None, anchor = None):
		"""Add a component to the frame with positioning,
		resizing	and scrolling options. See the manual for details."""
		self._place([item], left = left, right = right, top = top, bottom = bottom,
			sticky = sticky, scrolling = scrolling, border = border, anchor = anchor)
	
	def place_row(self, items,
			left = None, right = None, top = None, bottom = None,
			sticky = 'nw', scrolling = '', border = None, spacing = None,
			anchor = None):
		"""Add a row of components to the frame with positioning,
		resizing	and scrolling options. See the manual for details."""
		if left is not None and right is not None:
			raise ValueError("Cannot specify both left and right to place_row")
		elif left is None and right is not None:
			direction = 'left'
			items = items[:]
			items.reverse()
		else:
			direction = 'right'
		self._place(items, left = left, right = right, top = top, bottom = bottom,
			sticky = sticky, scrolling = scrolling, border = border,
			direction = direction, spacing = spacing, anchor = anchor)

	def place_column(self, items,
			left = None, right = None, top = None, bottom = None,
			sticky = 'nw', scrolling = '', border = None, spacing = None,
			anchor = None):
		"""Add a column of components to the frame with positioning,
		resizing	and scrolling options. See the manual for details."""
		if top is not None and bottom is not None:
			raise ValueError("Cannot specify both top and bottom to place_column")
		elif top is None and bottom is not None:
			direction = 'up'
			items = items[:]
			items.reverse()
		else:
			direction = 'down'
		self._place(items, left = left, right = right, top = top, bottom = bottom,
			sticky = sticky, scrolling = scrolling, border = border,
			direction = direction, spacing = spacing, anchor = anchor)

	def _place(self, items, 
			left = None,
			right = None,
			top = None,
			bottom = None,
			sticky = 'nw',
			scrolling = '',
			direction = 'right',
			spacing = None,
			border = None,
			anchor = None):
		
		def side(spec, name):
			#  Process a side specification taking the form of either
			#  (1) an offset, (2) a reference component, or (3) a
			#  tuple (component, offset). Returns a tuple (ref, offset)
			#  where ref is the reference component or None (representing
			#  the Frame being placed into). Checks that the reference
			#  component, if any, is directly contained by this Frame.
			ref = None
			offset = None
			if spec is not None:
				if isinstance(spec, tuple):
					ref, offset = spec
				elif isinstance(spec, Component):
					ref = spec
					offset = 0
				elif isinstance(spec, (int, float)):
					offset = spec
				else:
					raise ArgumentError(self, 'place', name, spec)
			if ref is self:
				ref = None
			elif ref:
				con = ref.container
				#if con is not self and isinstance(con, ScrollFrame):
				#	ref = con
				#	con = ref.container
				if con is not self:
					raise ValueError("Reference component for place() is not"
						" directly contained by the frame being placed into.")
			return ref, offset
		
		if spacing is None:
			spacing = self._place_default_spacing
		
		# Decode the sticky options
		if anchor is not None:
			sticky = anchor.translate(anchor_to_sticky)
		hmove = vmove = hstretch = vstretch = 0
		if 'e' in sticky:
			if 'w' in sticky:
				hstretch = 1
			else:
				hmove = 1
		if 's' in sticky:
			if 'n' in sticky:
				vstretch = 1
			else:
				vmove = 1
		
		# Translate the direction argument
		try:
			dir = {'right':0, 'down':1, 'left':2, 'up':3}[direction]
		except KeyError:
			raise ArgumentError(self, 'place', 'direction', direction)
			
		# Unpack the side arguments
		left_obj, left_off = side(left, 'left')
		right_obj, right_off = side(right, 'right')
		top_obj, top_off = side(top, 'top')
		bottom_obj, bottom_off = side(bottom, 'bottom')
		
		# Process the items
		#if not isinstance(items, list):
		#	items = [items]
		for item in items:
			x, y = item.position
			w, h = item.size
			# Calculate left edge position
			if left_obj:
				l = left_obj.left + left_obj.width + left_off
			elif left_off is not None:
				if left_off < 0:
					l = self.width + left_off
				else:
					l = left_off
			else:
				l = None
			# Calculate top edge position
			if top_obj:
				t = top_obj.top + top_obj.height + top_off
			elif top_off is not None:
				if top_off < 0:
					t = self.height + top_off
				else:
					t = top_off
			else:
				t = None
			# Calculate right edge position
			if right_obj:
				r = right_obj.left + right_off
			elif right_off is not None:
				if right_off <= 0:
					r = self.width + right_off
				else:
					r = right_off
			else:
				r = None
			# Calculate bottom edge position
			if bottom_obj:
				b = bottom_obj.top + bottom_off
			elif bottom_off is not None:
				if bottom_off <= 0:
					b = self.height + bottom_off
				else:
					b = bottom_off
			else:
				b = None
			# Fill in unspecified positions
			if l is None:
				if r is not None:
					l = r - w
				else:
					l = x
			if r is None:
				r = l + w
			if t is None:
				if b is not None:
					t = b - h
				else:
					t = y
			if b is None:
				b = t + h
			if scrolling:
				item.scrolling = scrolling
			# Position, resize and add the item
			item.bounds = (l, t, r, b)
			self.add(item)
			# Record resizing and border options
			item.hmove = hmove
			item.vmove = vmove
			item.hstretch = hstretch
			item.vstretch = vstretch
			if border is not None:
				item.border = border
			# Step to the next item
			if dir == 0:
				left_obj = item
				left_off = spacing
			elif dir == 1:
				top_obj = item
				top_off = spacing
			elif dir == 2:
				right_obj = item
				right_off = -spacing
			else:
				bottom_obj = item
				bottom_off = -spacing

	#
	#		Resizing
	#
	
	def _resized(self, delta):
		if self._auto_layout:
			self.resized(delta)

	def resized(self, delta):
		for c in self._contents:
			c.container_resized(delta)
	
	def resize(self, auto_layout = False, **kwds):
		"""Change the geometry of the component, with control over whether
		the layout of subcomponents is updated. The default is not to do so.
		Keyword arguments to this method may be any of the properties
		affecting position and size (i.e. left, top, right, bottom, x, y,
		width, height, position, size, bounds)."""
		old_auto_layout = self.auto_layout
		try:
			self.auto_layout = auto_layout
			self.set(**kwds)
		finally:
			self.auto_layout = old_auto_layout
		
	#
	#   Tabbing
	#
	
	def _build_tab_chain(self, chain):
		Component._build_tab_chain(self, chain)
		for c in self._contents:
			c._build_tab_chain(chain)

	#
	#   Other
	#
	
	def shrink_wrap(self, padding = None):
		"""Adjust the size of the component so that it neatly encloses its
		contents. If padding is specified, it specifies the amount of space
		to leave at right and bottom, otherwise the minimum distance from the
		left and top sides to the nearest components is used."""
		contents = self.contents
		if not contents:
			return
		if padding:
			hpad, vpad = padding
		else:
			hpad = min([item.left for item in contents])
			vpad = min([item.top for item in contents])
		rights = [item.right for item in contents]
		bottoms = [item.bottom for item in contents]
		self.resize(size = (max(rights) + hpad, max(bottoms) + vpad))
	
	def broadcast(self, message, *args):
		"""Traverse the component hierarchy, calling each component's handler for
		the given message, if any."""
		Component.broadcast(self, message, *args)
		for comp in self._contents:
			comp.broadcast(message, *args)
