from GUI import Window, TextField, Button, application
from testing import say

def show(tf):
	say("Text = %r" % tf.text)

def make_window():
	win = Window(size = (240, 100), title = "Password")
	tf = TextField(position = (20, 20), width = 200, password = True)
	ok = Button("OK", position = (20, 60),	action = (show, tf))
	win.add(tf)
	win.add(ok)
	win.show()

make_window()

instructions = """
There should be a window containing a password entry field.
Text in the field should be obfuscated, and it should not be
possible to copy text out of the field. The OK button should
cause the contents of the field to be reported.
"""

say(instructions)

application().run()
