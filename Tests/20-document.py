from GUI import Application, Window, Document, View, rgb, application
from testing import say

class TestDoc(Document):

	color = rgb(0.5, 0.5, 0.5)

	def set_color(self, c):
		self.color = c
		self.changed()
		self.notify_views()


class TestDocView(View):

	def draw(self, c, r):
		r = self.viewed_rect()
		#say("TestDocView.draw: viewed_rect =", r)
		m = self.model
		c.forecolor = m.color
		c.fill_rect(self.viewed_rect())

	def mouse_down(self, e):
		l, t, r, b = self.viewed_rect()
		x, y = e.position
		red = float(x - l) / float(r - l)
		green = float(r - x) / float(r - l)
		blue = float(y - b) / float(t - b)
		self.model.set_color(rgb(red, green, blue))


def test():
	doc = TestDoc(title = "Document")
	view = TestDocView(model = doc, size = (200, 200))
	win = Window(resizable = 0, size = (200, 200))
	win.add(view)
	win.document = doc
	#say(view.x, view.y, view.width, view.height)
	win.show()
	application().run()

instructions = """
There should be a window titled 'Document'.

Clicking in the window should cause it to be filled with a colour
that depends on the position of the click. On closing the window
or quitting the application, if the window has been clicked,
you should be asked whether to save changes. Cancelling should
prevent the close or quit.
"""

say(instructions)
test()
