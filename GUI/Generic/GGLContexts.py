#
#   PyGUI - OpenGL Contexts - Generic
#

from GUI.Properties import overridable_property
from GUI.GLShareGroups import ShareGroup

_current_share_group = None

class GLContext(object):
	"""Abstract base class for objects having an OpenGL context."""
	#
	#  _share_group  ShareGroup
	#
	
	share_group = overridable_property('share_group',
		"ShareGroup to which this context should belong, or None.")
	
	def __init__(self, share_group):
		if not share_group:
			share_group = ShareGroup()
		self._share_group = share_group
		if share_group:
			share_group._add(self)
	
	def destroy(self):
		pass
	
	def init_context(self):
		"""This method is called once after the associated OpenGL context
		is created. When called, this object's OpenGL context is the current
		context and the viewport is set to (0, 0, width, height). This method
		may be used to establish any desired initial OpenGL state."""
		pass
	
	def get_share_group(self):
		return self._share_group
	
	def _get_shared_context(self):
		"""Return another arbitrarily-chosen member of the share group of this
		context, or None if this context has no share group or there are no
		other members."""
		return self._share_group._some_member(exclude = self)
	
	def with_context(self, proc, flush = False):
		"""The proc should be a callable object of no arguments. Calls
		the proc with the associated OpenGL context as the current context.
		If flush is true, after calling proc, a glFlush followed by a
		buffer flush or swap is performed as appropriate."""
		self._with_context(proc, flush)

	def _with_context(self, proc, flush):
		#  Subclasses override this to implement with_context.
		#  Should call _with_share_group(proc).
		#  Signature can be changed if with_context is overridden to match.
		raise NotImplementedError
	
	def _with_share_group(self, proc):
		global _current_share_group
		old_share_group = _current_share_group
		_current_share_group = self._share_group
		try:
			proc()
		finally:
			_current_share_group = old_share_group


def current_share_group():
	group = _current_share_group
	if not group:
		raise ValueError("No current PyGUI OpenGL context")
	return group
