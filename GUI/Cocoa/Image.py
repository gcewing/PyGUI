#
#		Python GUI - Images - Cocoa
#

from Foundation import NSData
from AppKit import NSImage, NSBitmapImageRep
from GUI import export
from GUI.GImages import Image as GImage

class Image(GImage):
	#  _ns_bitmap_image_rep

	def _init_from_file(self, file):
		#ns_image = NSImage.alloc().initWithContentsOfFile_(file)
		#if not ns_image:
		ns_data = NSData.dataWithContentsOfFile_(file)
		if not ns_data:
			raise EnvironmentError("Unable to read image file: %s" % file)
		ns_rep = NSBitmapImageRep.imageRepWithData_(ns_data)
		if not ns_rep:
			raise ValueError("Unrecognised image file type: %s" % file)
		ns_rep.setSize_((ns_rep.pixelsWide(), ns_rep.pixelsHigh()))
		self._init_from_ns_rep(ns_rep)
	
	def _init_from_ns_rep(self, ns_rep):
		ns_image = NSImage.alloc().init()
		ns_image.addRepresentation_(ns_rep)
		self._ns_bitmap_image_rep = ns_rep
		self._init_with_ns_image(ns_image, flipped = True)

export(Image)
