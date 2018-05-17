from GUI import Window, ModalDialog, Label, Button, \
	TextField, application
from GUI.StdButtons import DefaultButton, CancelButton
from testing import say

def modal_dialog():
	#global dlog ###
	dlog = ModalDialog(title = "Spanish Inquisition", size = (200, 140))
	dlog.place(Label(text = "Surprise!!!"), left = 20, top = 20)
	field = TextField()
	dlog.place(field, left = 20, top = 60, right = -20)
	field.become_target()
	dlog.default_button = DefaultButton()
	dlog.cancel_button = CancelButton()
	dlog.place(dlog.default_button, right = -20, bottom = -20)
	dlog.place(dlog.cancel_button, left = 20, bottom = -20)
	dlog.center()
	result = dlog.present()
	say("Result =", result)
	dlog.destroy()

win = Window(title = "Modal Dialogs", size = (200, 60))
dialog_button = Button(title = "Give Me A Dialog", action = modal_dialog)
win.place(dialog_button, left = 20, top = 20)
win.show()

instructions = """
Clicking the "Give Me A Dialog" button should pop up a modal
dialog centered on the screen, containing a label, a text
field, an OK button and a Cancel button.

While the dialog is up:
* Interaction with the main window should be prevented.
* Edit menu commands should be enabled as appropriate for the
  text field; other menu commands should be disabled.

Clicking the OK button or pressing Return or Enter should
dismiss the dialog and report "Result = True".

Clicking the Cancel button or pressing Escape should
dismiss the dialog and report "Result = False".

On platforms without an application-wide menu bar, there should be
no menu bar in the window. However, the keyboard equivalents of the
edit menu commands should still work.
"""

say(instructions)
application().run()
