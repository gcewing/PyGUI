#
#   Python GUI - Pixmap - Gtk
#

from gtk import gdk
from GUI import export
from GUI.GtkPixmaps import GtkPixmap
from GUI.GPixmaps import Pixmap as GPixmap

class Pixmap(GtkPixmap, GPixmap):

	def __init__(self, width, height):
		GtkPixmap.__init__(self, width, height)

export(Pixmap)
