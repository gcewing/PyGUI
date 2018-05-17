#--------------------------------------------------------------------------
#
#		Python GUI - Pixmaps - Win32
#
#--------------------------------------------------------------------------

import GDIPlus as gdi
from GUI import export
from GUI import Canvas
from GUI.GPixmaps import Pixmap as GPixmap

class Pixmap(GPixmap):

	def __init__(self, width, height):
		self._win_image = gdi.Bitmap(width, height)

	def with_canvas(self, proc):
		proc(Canvas._from_win_image(self._win_image))

export(Pixmap)
