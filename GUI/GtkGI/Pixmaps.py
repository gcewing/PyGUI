#
#   Python GUI - Pixmap - Gtk
#

from gi.repository import Gdk
from GUI.GtkPixmaps import GtkPixmap
from GUI.GPixmaps import Pixmap as GPixmap

class Pixmap(GtkPixmap, GPixmap):

	def __init__(self, width, height):
		GtkPixmap.__init__(self, width, height)
