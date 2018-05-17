# This program is based on the color.c program written by Naofumi.

import os, sys
from GUI import Window, application
from GUI.GL import GLView, GLConfig
from OpenGL.GL import glClearColor, glClear, glBegin, glColor3f, glVertex2i, glEnd, \
	GL_COLOR_BUFFER_BIT, GL_TRIANGLES
from TestInput import TestKeyEvents, TestMouseEvents
from testing import say

class TriangleView(TestKeyEvents, TestMouseEvents, GLView):

	def init_context(self):
		glClearColor(0.0, 0.0, 0.0, 0.0)
		
	def render(self):
		glClear(GL_COLOR_BUFFER_BIT)
		glBegin(GL_TRIANGLES)
		glColor3f(1.0, 0.0, 0.0)
		glVertex2i(0, 1)
		glColor3f(0.0, 1.0, 0.0)
		glVertex2i(-1, -1)
		glColor3f(0.0, 0.0, 1.0)
		glVertex2i(1, -1)
		glEnd()

def make_view(db, options):
	pf = GLConfig(double_buffer = db)
	pf.alpha = "a" in options
	pf.depth_buffer = "d" in options
	pf.stencil_buffer = "s" in options
	pf.aux_buffers = "x" in options
	pf.accum_buffer = "A" in options
	view = TriangleView(pf, size = (200, 200))
	win = Window(
		title = "%s Buffered GLView" % ["Single", "Double"][db],
		size = (240, 240))
	win.place(view, left = 20, top = 20, sticky = "nsew")
	view.become_target()
	win.show()

def get_args():
	args = sys.argv[1:]
	if not 0 <= len(args) <= 2:
		badusage()
	if args:
		sd = args[0][0]
	else:
		sd = "d"
	if sd == "s":
		db = False
	elif sd == "d":
		db = True
	else:
		badusage()
	if len(args) > 1:
		options = args[1]
	else:
		options = ""
	return db, options

def badusage():
	sys.stderr.write("Usage: python %s s[ingle]|d[ouble] [adsxA]\n" % os.path.basename(sys.argv[0]))
	sys.exit(1)

instructions = """
There should be a window containing an OpenGL view, 20 pixels
from the edge of the window on all sides. There should be a
coloured triangle filling the view over a black background.

Mouse and keyboard events in the view should be reported.
The view and the triangle it contains should resize smoothly
with the window.
"""

make_view(*get_args())
say(instructions)
application().run()
