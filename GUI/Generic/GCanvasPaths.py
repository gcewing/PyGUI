#
#   Python GUI - Canvas Paths - Generic
#

class CanvasPaths:
	#  Mixin class providing generic implementations of
	#  canvas path construction operators.
	
	def __init__(self):
		self.newpath()

	def newpath(self):
		self._path = []
		self._current_subpath = None
		self._current_point = (0, 0)
	
	def moveto(self, x, y):
		self._current_subpath = None
		self._current_point = self._coords(x, y)
	
	def rmoveto(self, dx, dy):
		x, y = self._current_point
		self.moveto(x + dx, y + dy)
	
	def lineto(self, x, y):
		subpath = self._current_subpath
		if subpath is None:
			subpath = [self._current_point]
			self._path.append(subpath)
			self._current_subpath = subpath
		p = self._coords(x, y)
		subpath.append(p)
		self._current_point = p
	
	def rlineto(self, dx, dy):
		x, y = self._current_point
		self.lineto(x + dx, y + dy)
	
	def closepath(self):
		subpath = self._current_subpath
		if subpath:
			subpath.append(subpath[0])
			self._current_subpath = None
	
	def get_current_point(self):
		return self._current_point
	
	#  Implementations may set _coords to one of the following
	
	def _int_coords(self, x, y):
		return int(round(x)), int(round(y))
	
	def _float_coords(self, x, y):
		return x, y

