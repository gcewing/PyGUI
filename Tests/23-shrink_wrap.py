from GUI import Window, Button, CheckBox, TextField, application
from testing import say

def test():
	def bing():
		say("Bing!")
		#fld._win_dump_flags()
	win = Window(title = "Shrink Wrap", resizable = 0)
	but = Button("Bing!", action = bing)
	cbx = CheckBox("Spam")
	fld = TextField(width = 100)
	win.place(but, left = 20, top = 20)
	win.place(cbx, left = but + 20, top = 20)
	win.place(fld, left = 20, top = but + 20)
	win.shrink_wrap()
	win.show()
	application().run()


instructions = """
There should be a window containing three controls, with the window
sized to fit the controls with 20 pixels of space on all sides.
"""

say(instructions)
test()
