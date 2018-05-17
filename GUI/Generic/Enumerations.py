#
#   PyGUI - Enumerated type facilities
#

class EnumMap(dict):

	def __init__(self, __name__, *args, **kwds):
		self.name = __name__
		dict.__init__(self, *args, **kwds)
	
	def __getitem__(self, key):
		try:
			return dict.__getitem__(self, key)
		except KeyError:
			raise ValueError("Invalid %s '%s', should be one of %s" %
				(self.name, key, ", ".join(["'%s'" % val for val in self.keys()])))
