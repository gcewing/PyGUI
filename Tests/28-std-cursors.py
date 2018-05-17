#
#   Standard cursors test
#

from GUI import Window, View, \
	RadioGroup, RadioButton, application #, StdCursors
from GUI.StdColors import black, white
from testing import say

class TestArea(View):

	def draw(self, c, r):
		c.forecolor = white
		c.fill_rect(r)
		c.forecolor = black
		w, h = self.size
		c.frame_rect((0, 0, w, h))

def test():
	def select():
		i = group.value
		name = cursor_names[i]
		say("Selecting cursor no. %d (%s)" % (i, name))
		cursor = getattr(StdCursors, name)
		say("...", cursor)
		view.cursor = cursor
	win = Window(title = "Std Cursors")
	view = TestArea(size = (100, 100))
	win.place(view, left = 20, top = 20)
	group = RadioGroup(action = select)
	for i, name in enumerate(cursor_names):
		group.add_item(RadioButton(title = name, value = i))
	win.place_column(group, left = view + 20, top = 20, spacing = 0)
	win.shrink_wrap((20, 20))
	win.show()
	application().run()

app = application()
from GUI import StdCursors
cursor_names = []
for name in StdCursors.__all__:
		cursor_names.append(name)
test()
