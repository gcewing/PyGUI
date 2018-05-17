#
#		Python GUI - Standard Cursors - Gtk
#

from gtk import gdk
from GUI import Cursor

__all__ = [
	'arrow',
	'ibeam', 
	'crosshair', 
	'fist', 
	'hand', 
	'finger', 
	'invisible', 
]

arrow = Cursor._from_gtk_std_cursor(gdk.LEFT_PTR)
ibeam = Cursor._from_gtk_std_cursor(gdk.XTERM)
crosshair = Cursor._from_gtk_std_cursor(gdk.TCROSS)
fist = Cursor("cursors/fist.tiff")
hand = Cursor("cursors/hand.tiff")
finger = Cursor("cursors/finger.tiff")
invisible = Cursor._from_nothing()

del gdk
del Cursor

def empty_cursor():
	return invisible
