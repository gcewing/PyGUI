from __future__ import division
from math import sin, pi
from numpy import zeros, uint8
from GUI import Window, View, application, rgb
from GUI.StdColors import yellow
from GUI.Numerical import image_from_ndarray
from GUI.Geometry import offset_rect
from testing import say

background = rgb(0.25, 0.25, 0.25)

width = 300
height = 100

def plot(a, f, c):
	h = height // 2
	A = h - 1
	for x in xrange(width):
		y = h + int(round(A * sin(2 * pi * f * x / width)))
		a[y, x] = c

def make_array():
	a = zeros((height, width, 4), uint8)
	plot(a, 1, (255, 0, 0, 255))
	plot(a, 2, (255, 255, 0, 255))
	plot(a, 3, (0, 255, 0, 255))
	return a

the_array = make_array()
the_image = image_from_ndarray(the_array, 'RGBA')

class ImageTestView(View):

	def draw(self, c, r):
		image = the_image
		c.backcolor = background
		c.erase_rect(r)
		main_image_pos = (10, 10)
		src_rect = image.bounds
		#say("Image bounds =", src_rect)
		dst_rect = offset_rect(src_rect, main_image_pos)
		#say("Drawing", src_rect, "in", dst_rect)
		image.draw(c, src_rect, dst_rect)

win = Window(size = (width + 20, height + 20), title = "Image from NumPy Array")
view = ImageTestView(size = win.size)
win.add(view)
view.become_target()
win.show()

instructions = """
There should be a red, a yellow and a green sinewave on a grey background.
"""

say(instructions)
application().run()
