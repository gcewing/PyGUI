from GUI import Window, View, Image, application
from GUI.Geometry import offset_rect, rect_sized
from GUI.StdColors import yellow
from testing import say


class ImageTestView(View):

	def draw(self, c, r):
		c.backcolor = yellow
		c.erase_rect(r)
		main_image_pos = (10, 10)
		src_rect = image.bounds
		#say("Image bounds =", src_rect)
		dst_rect = offset_rect(src_rect, main_image_pos)
		#say("Drawing", src_rect, "in", dst_rect)
		image.draw(c, src_rect, dst_rect)
		src_rect = rect_sized((180, 160), (100, 100))
		c.frame_rect(offset_rect(src_rect, main_image_pos))
		dst_rect = rect_sized((10, 340), (150, 150))
		#say("Drawing", src_rect, "in", dst_rect)
		image.draw(c, src_rect, dst_rect)
		dst_rect = rect_sized((200, 340), (100, 100))
		#say("Drawing", src_rect, "in", dst_rect)
		image.draw(c, src_rect, dst_rect)
		dst_rect = rect_sized((340, 340), (50, 50))
		#say("Drawing", src_rect, "in", dst_rect)
		image.draw(c, src_rect, dst_rect)

import os, sys
here = sys.path[0]
image_path = os.path.join(here, "imac.jpg")
image = Image(file = image_path)

win = Window(size = (500, 500))
view = ImageTestView(size = win.size)
win.add(view)
view.become_target()
win.show()

instructions = """
There should be a 360x264 image of an iMac with a rectangle drawn
around part of the image. This part should appear at three different
sizes (150x150, 100x100, 50x50) below the main image.
"""

say(instructions)
application().run()
