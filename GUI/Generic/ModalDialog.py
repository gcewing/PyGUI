#
#   Python GUI - Modal Dialogs - Generic
#

from GUI import application, export
from GUI import Dialog

class ModalDialog(Dialog):

	def __init__(self, style = 'modal_dialog', **kwds):
		Dialog.__init__(self, style = style, **kwds)
	
	def present(self):
		self._result = None
		self._dismissed = 0
		self.show()
		app = application()
		try:
			while not self._dismissed:
				self.modal_event_loop()
		finally:
			self.hide()
		return self._result
	
	def dismiss(self, result = 0):
		self._result = result
		self._dismissed = 1
		self.exit_modal_event_loop()
	
	def close_cmd(self):
		self.dismiss()

	def next_handler(self):
		return None

	def ok(self):
		self.dismiss(True)
	
	def cancel(self):
		self.dismiss(False)

export(ModalDialog)
