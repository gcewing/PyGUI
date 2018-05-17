from GUI import ModalDialog, Label, Button, Task, application

class NagBox(ModalDialog):

	def __init__(self, text, timeout):
		ModalDialog.__init__(self)
		label = Label(text)
		self.ok_button = Button("OK", action = "ok", enabled = False)
		self.place(label, left = 20, top = 20)
		self.place(self.ok_button, top = label + 20, right = label.right)
		self.shrink_wrap(padding = (20, 20))
		self.timer = Task(self.enable_button, timeout)
	
	def enable_button(self):
		self.ok_button.enabled = True
	
	def ok(self):
		self.dismiss(True)


dlog = NagBox("Consider yourself nagged.", 10)
dlog.present()
