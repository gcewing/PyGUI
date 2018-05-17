#
#		User-defined views used by test programs
#

from GUI import View, Color, Font
from GUI.StdFonts import system_font, application_font
from GUI.StdColors import black, red, green, blue, yellow, white
from testing import say

fancy_font = Font("Times", 48, ['italic'])
#fancy_font = Font("Courier New", 48)
#fancy_font = Font("Courier", 48)

class TestDrawing(View):

	def draw(self, c, r):
		c.backcolor = yellow
		c.erase_rect((0, 0, self.width, self.height))
		self.draw_triangle(c, 10, 40, red)
		c.gsave()
		c.rectclip((100, 0, 120, 50))
		self.draw_triangle(c, 100, 40, green)
		c.grestore()
		self.draw_triangle(c, 50, 100, blue)
		f1 = system_font
		f2 = application_font
		f3 = fancy_font
		self.draw_text(c, 150, 100, f1, "System Font")
		self.draw_text(c, 150, 120, f2, "Application Font")
		self.draw_text(c, 5, 180, f3, "Times Italic 48")

	def draw_text(self, c, x, y, f, s):
		a = f.ascent
		d = f.descent
		#say("Font size", f.size, "ascent", a, "descent", d)
		w = f.width(s)
		c.fill_rect((x, y - a - 1, x + w, y - a))
		c.fill_rect((x, y, x + w, y + 1))
		c.fill_rect((x, y + d, x + w, y + d + 1))
		c.font = f
		c.moveto(x, y)
		c.show_text(s)
	
	def triangle_path(self, c, x, y):
		c.newpath()
		c.moveto(x, y)
		c.rlineto(40, 0)
		c.rlineto(-20, -30)
		c.closepath()

	def draw_triangle(self, c, x, y, hue):
		self.triangle_path(c, x, y)
		c.forecolor = hue
		c.fill()
		self.triangle_path(c, x, y)
		c.pensize = 3
		c.forecolor = black
		c.stroke()

	def fill_rectangle(self, c, rect, hue):
		(l, t, r, b) = rect
		c.newpath()
		c.moveto(l, t)
		c.lineto(l, b)
		c.lineto(r, b)
		c.lineto(r, t)
		c.closepath()
		c.forecolor = hue
		c.fill()


