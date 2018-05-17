from GUI import Window, GridView, run
from testing import say

class TestGridView(GridView):

	def __init__(self):
		GridView.__init__(self, num_rows = 10, num_columns = 5,
			cell_size = (50, 20), anchor = 'ltrb')
		self.content_size = self.extent
	
	def draw_cell(self, c, row, col, rect):
		x = rect[0] + 5
		y = rect[1] + 15
		t = "Cell %d,%d" % (row, col)
		c.frame_rect(rect)
		c.moveto(x, y)
		c.show_text(t)

	def click_cell(self, row, col, event):
		print "Cell %d,%d clicked" % (row, col)


win = Window(title = "Grid View")
view = TestGridView()
win.add(view)
win.shrink_wrap()
win.show()

instructions = """
There should be a grid view with 10 rows and 5 columns.
The row and column numbers of clicked cells should be reported.
"""

say(instructions)
run()
