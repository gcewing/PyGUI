#------------------------------------------------------------------------------
#
#		Python GUI - Properties - Generic
#
#------------------------------------------------------------------------------

class Properties(object):
	"""
	This class implements the standard interface for initialising
	properties using keyword arguments.
	"""

	def __init__(self, **kw):
		"Properties(name=value, ...) passes the given arguments to the set() method."
		self.set(**kw)

	def set(self, **kw):
		"""set(name=value, ...) sets property values according to the given 
		keyword arguments. Will only set attributes for which a descriptor exists."""
		cls = self.__class__
		for name, value in kw.iteritems():
			try:
				s = getattr(cls, name).__set__
			except AttributeError:
				raise TypeError("%s object has no writable property %r" % (
					self.__class__.__name__, name))			
			s(self, value)

#------------------------------------------------------------------------------

def overridable_property(name, doc = None):
	"""Creates a property which calls methods get_xxx and set_xxx of
	the underlying object to get and set the property value, so that
	the property's behaviour may be easily overridden by subclasses."""
	
	getter_name = intern('get_' + name)
	setter_name = intern('set_' + name)
	return property(
		lambda self: getattr(self, getter_name)(),
		lambda self, value: getattr(self, setter_name)(value),
		None,
		doc)
