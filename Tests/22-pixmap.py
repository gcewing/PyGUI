from GUI import Window, View, Pixmap, application
from GUI.Geometry import offset_rect, rect_sized
from GUI.StdColors import red, yellow, green, blue, cyan, black
from testing import say

class PixmapTestView(View):

	def draw(self, c, r):
		c.erase_rect(r)
		main_image_pos = (10, 10)
		src_rect = pixmap.bounds
		dst_rect = offset_rect(src_rect, main_image_pos)
		pixmap.draw(c, src_rect, dst_rect)
		src_rect = rect_sized((180, 160), (100, 100))
		c.frame_rect(offset_rect(src_rect, main_image_pos))
		dst_rect = rect_sized((10, 340), (150, 150))
		pixmap.draw(c, src_rect, dst_rect)
		dst_rect = rect_sized((200, 340), (100, 100))
		pixmap.draw(c, src_rect, dst_rect)
		dst_rect = rect_sized((340, 340), (50, 50))
		pixmap.draw(c, src_rect, dst_rect)


def do_test_drawing(c):
	b = pixmap.bounds
	c.forecolor = cyan
	c.fill_rect(b)
	r = (20, 20, 200, 230)
	c.forecolor = red
	c.fill_rect(r)
	r = (160, 90, 300, 180)
	c.forecolor = yellow
	c.fill_rect(r)
	r = (250, 200, 350, 275)
	c.forecolor = blue
	c.fill_oval(r)
	
instructions = """
There should be a 400x300 image containing a filled red rectangle,
yellow rectangle and blue oval on a cyan background, with a black
frame around part of the image. The framed part should appear below
in three different sizes, 150x150, 100x100 and 50x50.
"""

say(instructions)

app = application()

pixmap = Pixmap(400, 300)
pixmap.with_canvas(do_test_drawing)

win = Window(title = "Pixmap", size = (500, 500))
view = PixmapTestView(size = win.size)
win.add(view)
win.show()

app.run()
