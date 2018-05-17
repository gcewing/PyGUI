#
#		Python GUI - Standard Cursors - Gtk
#

from gi.repository import Gdk
from GUI.Cursors import Cursor

__all__ = [
	'arrow',
	'ibeam', 
	'crosshair', 
	'fist', 
	'hand', 
	'finger', 
	'invisible', 
]

arrow = Cursor._from_gtk_std_cursor(Gdk.CursorType.LEFT_PTR)
ibeam = Cursor._from_gtk_std_cursor(Gdk.CursorType.XTERM)
crosshair = Cursor._from_gtk_std_cursor(Gdk.CursorType.TCROSS)
fist = Cursor("cursors/fist.tiff")
hand = Cursor("cursors/hand.tiff")
finger = Cursor("cursors/finger.tiff")
invisible = Cursor._from_nothing()

del Cursor

def empty_cursor():
	return invisible
