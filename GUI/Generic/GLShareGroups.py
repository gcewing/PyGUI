#
#   PyGUI - OpenGL Context Sharing - Generic
#

from weakref import WeakKeyDictionary

class ShareGroup(object):
	"""Object representing a shared texture and display list
	namespace for OpenGL contexts."""
	
	def __init__(self):
		self.contexts = WeakKeyDictionary()
	
	def __contains__(self, context):
		"Test whether a GLView or GLPixmap is a member of this share group."
		return context in self.contexts
	
	def __iter__(self):
		"Return an iterator over the members of this share group."
		return iter(self.contexts)

	def _add(self, context):
		self.contexts[context] = 1
	
	def _some_member(self, exclude = None):
		for member in self.contexts:
			if member is not exclude:
				return member
		return None
