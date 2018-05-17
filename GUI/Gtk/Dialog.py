#
#   Python GUI - Dialogs - Gtk
#

from GUI import export
from GUI.GDialogs import Dialog as GDialog

class Dialog(GDialog):

	_default_keys = ['\r']
	_cancel_keys = ['\x1b']

export(Dialog)
