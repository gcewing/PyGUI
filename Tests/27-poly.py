from GUI import Window, View, application
from GUI.StdColors import green, black, white
from testing import say

class PolyView(View):

	def draw(self, c, r):
		points = [(10, 10), (20, 100), (50, 90), (100, 50), (40, 40)]
		c.forecolor = white
		c.fill_rect(r)
		c.forecolor = green
		c.fill_poly(points)
		c.forecolor = black
		c.stroke_poly(points)


def main():
	win = Window()
	view = PolyView(width = 120, height = 120)
	win.add(view)
	win.shrink_wrap()
	win.show()
	application().run()

instructions = """
There should be a window containing an irregularly-shaped
polygon filled with green and outlined in black.
"""

say(instructions)
main()
