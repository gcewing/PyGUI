from GUI import Window, Button, application
from GUI.Exceptions import ApplicationError
from testing import say

class ShrubberyError(Exception):
	pass

def raise_application_error():
	raise ApplicationError("Your underpants are on fire.",
		"Please notify the fire service and proceed in an orderly manner to the nearest exit.")

def raise_exception():
	raise ShrubberyError("The shrubbery is too small.")

def test():
	win = Window(title = "Exceptions", size = (200, 100))
	but1 = Button("ApplicationError", action = raise_application_error)
	but2 = Button("Exception", action = raise_exception)
	win.place_column([but1, but2], left = 20, top = 20)
	win.shrink_wrap(padding = (20, 20))
	win.show()
	application().run()

instructions = """
Pressing the ApplicationError button will raise an ApplicationError.
An alert box should appear displaying message and detail strings.

Pressing the Exception button will raise an exception. A dialog box
should appear containing a description of the exception and options
Continue, Traceback and Abort. Continue should continue the application
with no further action. Traceback should print a traceback to the
console and then continue. Abort should print a traceback and exit
the application.
"""

say(instructions)
test()
