#--------------------------------------------------------------------------
#
#		Python GUI - Cursors - Generic
#
#--------------------------------------------------------------------------

from GUI.Properties import Properties
from GUI.Resources import lookup_resource, find_resource, get_resource
from GUI import Image

def _hotspot_for_resource(resource_name):
	path = lookup_resource(resource_name, "hot")
	if path:
		f = open(path, "rU")
		xs, ys = f.readline().split()
		return int(xs), int(ys)
	else:
		return None

class Cursor(Properties):
	"""A Cursor is an image representing the mouse pointer.
	
	Constructors:
	    Cursor(resource_name, hotspot)
	    Cursor(image, hotspot)
	"""
	
	def from_resource(cls, name, hotspot = None, **kwds):
		def load(path):
			image = Image.from_resource(name, **kwds)
			return cls(image, hotspot or _hotspot_for_resource(name))
		return get_resource(load, name)
	
	from_resource = classmethod(from_resource)
	
	def __init__(self, spec, hotspot = None):
		"""Construct a Cursor from a resource or Image and a hotspot point.
		The hotspot defaults to the centre of the image."""
		if isinstance(spec, basestring):
			self._init_from_resource(spec, hotspot)
		else:
			self._init_from_image(spec, hotspot)

	def _init_from_resource(self, resource_name, hotspot):
		image = Image(file = find_resource(resource_name))
		if not hotspot:
			hotspot = _hotspot_for_resource(resource_name)
		self._init_from_image(image, hotspot)

	def _init_from_image(self, image, hotspot):
		if not hotspot:
			width, height = image.size
			hotspot = (width // 2, height // 2)
		self._init_from_image_and_hotspot(image, hotspot)

