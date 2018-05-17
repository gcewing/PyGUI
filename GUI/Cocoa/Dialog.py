#
#   Python GUI - Dialogs - Cocoa
#

from GUI import export
from GUI.GDialogs import Dialog #as GDialog

#class Dialog(GDialog):
#
#	_default_keys = ['\r']
#	_cancel_keys = ['\x1b']
#
#	def key_down(self, event):
#		# Cocoa already takes care of default/cancel button activation
#		self.pass_to_next_handler('key_down', event)

export(Dialog)
