from GUI import Window, View, application, rgb
from GUI.Geometry import offset_rect, rect_sized
from GUI.StdColors import yellow
from GUI.PIL import image_from_pil_image
import Image
from testing import say

from GUI import PIL
PIL.debug_pil = True

skyblue = rgb(102/255.0, 204/255.0, 1.0)

class ImageTestView(View):

	def draw(self, c, r):
		c.backcolor = skyblue
		c.erase_rect(r)
		main_image_pos = (50, 50)
		src_rect = image.bounds
		#say("Image bounds =", src_rect)
		dst_rect = offset_rect(src_rect, main_image_pos)
		#say("Drawing", src_rect, "in", dst_rect)
		image.draw(c, src_rect, dst_rect)

import os, sys
here = sys.path[0]
image_path = os.path.join(here, "pill.png")
pil_image = Image.open(image_path)
print "PIL Image: size =", pil_image.size, "mode =", pil_image.mode
image = image_from_pil_image(pil_image)

win = Window(size = (350, 200), title = "PIL Image")
view = ImageTestView(size = win.size)
win.add(view)
view.become_target()
win.show()

instructions = """
There should be an image of a red and yellow pill on a blue background.
The background should show through transparent areas of the image, and
the edges of the non-transparent areas should be smooth.
"""

say(instructions)
application().run()
