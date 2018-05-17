from GUI import Window, PaletteView, run
from testing import say

class TestPaletteView(PaletteView):

	def __init__(self):
		PaletteView.__init__(self, num_items = 10, items_per_row = 4,
			cell_size = (50, 30))
		
	def draw_item(self, c, i, rect):
		x = rect[0] + 5
		y = rect[1] + 15
		t = "Item %d" % i
		c.frame_rect(rect)
		c.moveto(x, y)
		c.show_text(t)
	
	def click_item(self, i, event):
		print "Item %d clicked" % i


win = Window(title = "Palette View")
view = TestPaletteView()
win.add(view)
win.shrink_wrap()
win.show()

instructions = """
There should be a palette view with 10 items arranged in 4 columns.
The item number of a clicked item should be reported.
"""

say(instructions)
run()
