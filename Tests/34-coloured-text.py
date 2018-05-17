#
#   PyGUI - Test coloured text drawing
#

from GUI import Window, View, StdColors, run
from testing import say

tests = [
	("Red", StdColors.red),
	("Green", StdColors.green),
	("Blue", StdColors.blue),
	("Cyan", StdColors.cyan),
	("Magenta", StdColors.magenta),
	("Yellow", StdColors.yellow),
]

class TestView(View):

	def draw(self, c, r):
		c.forecolor = StdColors.grey
		c.fill_rect(r)
		f = c.font
		x = 10
		y = 10 + f.ascent
		h = f.line_height
		for (text, color) in tests:
			c.moveto(x, y)
			c.textcolor = color
			c.show_text(text)
			y += h

def test():
	view = TestView(size = (300, 200))
	win = Window(title = "Coloured Text")
	win.add(view)
	win.shrink_wrap()
	win.show()
	run()
	
instructions = """
There should be a view showing text in a variety of colours.
"""

say(instructions)
test()
