#--------------------------------------------------------------------
#
#   PyGUI - Image - Win32
#
#--------------------------------------------------------------------

import GDIPlus as gdi
from GUI import export
from GUI.GImages import Image as GImage

class Image(GImage):

	def _init_from_file(self, path):
		self._win_image = gdi.Bitmap.from_file(path)

export(Image)
