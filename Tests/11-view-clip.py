#
#   Test user-defined views.
#

from GUI import Window, View, application
from GUI.StdColors import red
from testing import say

class View1(View):

	def draw(self, c, r):
		say("View1.draw")
		c.set_forecolor(red)
		c.fill_rect(self.viewed_rect())


def main():
	win = Window(size = (500, 400))
	view1 = View1(position = (10, 10), size = (200, 100))
	win.add(view1)
	win.show()
	application().run()
	
instructions = """
There should be 500x400 window with a 200x100 red filled rectangle
near the top left corner.
"""

say(instructions)
main()
