#
#   Python GUI - Dialogs - Gtk
#

from GUI.GDialogs import Dialog as GDialog

class Dialog(GDialog):

	_default_keys = ['\r']
	_cancel_keys = ['\x1b']
