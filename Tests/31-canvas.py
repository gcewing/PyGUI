#
#   PyGUI - Canvas primitives test
#

from GUI import Window, View, Menu, application
from GUI.StdMenus import basic_menus
from GUI.StdColors import black, white
from testing import say

r = 40
sa = 45
#aa = 240
ea = 270

class LineTest:

	menu_item = "Line/^L"
	
	def draw(self, c):
		c.newpath()
		c.moveto(10, 10)
		c.lineto(190, 290)
		c.stroke()


class RectTest:

	menu_item = "Rect/^R"
	
	def draw(self, c):
		c.stroke_rect((20, 20, 180, 80))
		c.frame_rect((20, 120, 180, 180))
		c.fill_rect((20, 220, 180, 280))


class OvalTest:

	menu_item = "Oval/^O"
	
	def draw(self, c):
		c.stroke_oval((20, 20, 180, 80))
		c.frame_oval((20, 120, 180, 180))
		c.fill_oval((20, 220, 180, 280))


class ArcTest:

	menu_item = "Arc/^A"
	
	def draw(self, c):
		c.stroke_arc((50, 50), r, sa, ea)
		c.frame_arc((50, 150), r, sa, ea)
		#c.fill_arc((50, 250), r, sa, ea)


class WedgeTest:

	menu_item = "Wedge/^W"
	
	def draw(self, c):
		c.stroke_wedge((50, 50), r, sa, ea)
		#c.frame_wedge((50, 150), r, sa, ea)
		c.fill_wedge((50, 250), r, sa, ea)

class BezierTest:

	menu_item = "Bezier/^B"

	def bez_path(self, c, x0, y0):
		c.newpath()
		c.moveto(x0, y0 + 40)
		c.rcurveto((50, -100), (100, 100), (150, 0))
		c.closepath()
	
	def draw(self, c):
		self.bez_path(c, 10, 10)
		c.stroke()
		self.bez_path(c, 10, 210)
		c.fill()


tests = [
	LineTest(),
	RectTest(),
	OvalTest(),
	ArcTest(),
	WedgeTest(),
	BezierTest(),
]


test_menu = Menu("Shape", [
	([t.menu_item for t in tests], 'test_cmd')
])


class CTV(View):

	test = None

	def draw(self, c, r):
		c.forecolor = white
		c.fill_rect(r)
		c.forecolor = black
		c.pensize = 10
		if self.test:
			self.test.draw(c)
	
	def setup_menus(self, m):
		m.test_cmd.enabled = True
	
	def test_cmd(self, i):
		self.test = tests[i]
		self.invalidate()


def main():
	view = CTV(size = (200, 300))
	win = Window(title = "Canvas")
	win.add(view)
	win.shrink_wrap()
	view.become_target()
	win.show()
	app = application()
	app.menus = basic_menus() + [test_menu]
	app.run()

instructions = """
The Line test should draw a straight diagonal line.
The other tests should each produce a stroked shape,
a framed shape and a filled shape where applicable.

Arcs should start 45 degrees clockwise from the x
axis and continue clockwise up to 270 degrees.
"""

say(instructions)
main()
