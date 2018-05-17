#
#		User-defined scrollable views used by test programs
#

from GUI import ScrollableView, Color, Font
from GUI.StdFonts import system_font, application_font
from GUI.StdColors import black, red, green, blue, yellow, white
from TestInput import TestKeyEvents, TestTrackMouse
from testing import say

bgc = [green, blue, yellow] ###
bgi = 0 ###

class TestScrollableDrawing(ScrollableView):

	report_update_rect = False

	def __init__(self, **kwds):
		ScrollableView.__init__(self, **kwds)
		self.extent = (1000, 1000)
	
	def blue_update_rgn(self, c):
		c.fillcolor = blue
		c.fill_rect(self.viewed_rect())

	def draw(self, c, r):
		if self.report_update_rect:
			say("Update rect =", r)
		viewed_rect = self.viewed_rect()
		c.fillcolor = white
		c.fill_rect(viewed_rect)
		c.pensize = 6
		c.fillcolor = red
		x = 20
		y = 10
		for i in range(0, 20):
			c.newpath()
			c.moveto(x - 20, y + 20)
			c.rlineto(80, -20)
			c.rlineto(-40, 60)
			c.closepath()
			c.fill()
			c.stroke()
			x += 80
			y += 80
		ew, eh = self.extent
		c.frame_rect((0, 0, ew, eh))


class TestScrollableView(TestKeyEvents, TestTrackMouse, TestScrollableDrawing):
	pass
