#
#   PyGUI - Test targeted() and untargeted() methods
#

from GUI import View, Window, application
from GUI.StdColors import red, green
from testing import say

class TestPatch(View):

	def __init__(self, name, color, **kwds):
		self.name = name
		self.color = color
		View.__init__(self, size = (60, 60), **kwds)
	
	def draw(self, c, r):
		c.forecolor = self.color
		c.fill_rect(r)
	
	def mouse_down(self, e):
		say("%s clicked" % self.name)
		self.become_target()
	
	def targeted(self):
		say("%s targeted" % self.name)

	def untargeted(self):
		say("%s untargeted" % self.name)

def test():
	win = Window(title = "Targeting", size = (180, 100))
	patch1 = TestPatch("Red patch", red, position = (20, 20))
	patch2 = TestPatch("Green patch", green, position = (100, 20))
	win.add(patch1)
	win.add(patch2)
	win.show()
	application().run()

instructions = """
There should be a window with two coloured patches. Clicking
in a patch will make it the target. Messages should be printed
whenever a patch is clicked or its target status changes.
"""

say(instructions)
test()
