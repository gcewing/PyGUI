from GUI import Window, ListButton, application
from testing import say

def report():
	print "Value =", but.value

but = ListButton(position = (20, 20),
	titles = ["Item %d" % i for i in xrange(30)],
	action = report)
but.value = 42
win = Window(title = "List Button")
win.add(but)
but.become_target()
win.show()

instructions = """
There should be a list button containing 30 items.
   
Selecting an item should cause its value to be reported. On Windows,
it should be possible to make a selection by typing the first letter
of the title.
"""

say(instructions)
application().run()
