from GUI import Window, View, application, rgb, Pixmap
from GUI.Geometry import offset_rect
from GUI.StdColors import black, white
from GUI.GL import GLPixmap
from OpenGL.GL import glClearColor, glClear, glBegin, glColor3f, glVertex2i, glEnd, \
	GL_COLOR_BUFFER_BIT, GL_TRIANGLES


class PixmapTestView(View):

	def __init__(self, pixmap, **kwds):
		self.pixmap = pixmap
		View.__init__(self, **kwds)
	
	def draw(self, c, r):
		#print "Draw" ###
		c.forecolor = rgb(0.5, 0.75, 1.0)
		c.fill_rect(self.viewed_rect())
		c.forecolor = black
		pm = self.pixmap
		sr = pm.bounds
		for i in range(3):
			dr = offset_rect(sr, (10 + i * 50, 10 + i * 60))
			pm.draw(c, sr, dr)


def draw_triangle():
	#print "Draw Triangle"
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	#return ###
	glBegin(GL_TRIANGLES)
	glColor3f(1.0, 0.0, 0.0)
	glVertex2i(0, 1)
	glColor3f(0.0, 1.0, 0.0)
	glVertex2i(-1, -1)
	glColor3f(0.0, 0.0, 1.0)
	glVertex2i(1, -1)
	glEnd()

def draw_circle(c):
	c.forecolor = white
	c.frame_oval((10, 10, 40, 40))

def test():
	app = application()
	pixmap = GLPixmap(50, 50, double_buffer = False, alpha = False)
	pixmap.with_context(draw_triangle, flush = True)
	#pixmap.with_canvas(draw_circle)
	view = PixmapTestView(pixmap, size = (180, 200))
	win = Window(title = "GLPixmap", resizable = False)
	win.add(view)
	win.shrink_wrap()
	win.show()
	app.run()

instructions = """
You should see a multicoloured triangle inside a black square,
repeated three times over a blue background.
"""

print instructions
test()
