# A translation of the gears demo that comes with mesa.
# Conversion from gtk.gl module to PyGtkGLExt by Naofumi Yasufuku
# Conversion to PyGUI by Greg Ewing

import math
from GUI import Window, Task, application
from GUI.GL import GLView
from OpenGL import GL

frame_interval = 0.01
rotation_step = 5.0

rotations = {
	'up_arrow':    (-rotation_step, 0.0, 0.0),
	'down_arrow':  ( rotation_step, 0.0, 0.0),
	'left_arrow':  (0.0, -rotation_step, 0.0),
	'right_arrow': (0.0,  rotation_step, 0.0),
}

#----------------------------------------------------------------------------

# Draw a gear wheel.	You'll probably want to call this function when
# building a display list since we do a lot of trig here.
#
#  Input:
#    inner_radius - radius of hole at center
#    outer_radius - radius at center of teeth
#    width - width of gear
#    teeth - number of teeth
#    tooth_depth - depth of tooth
def gear(inner_radius, outer_radius, width, teeth, tooth_depth):
		cos = math.cos
		sin = math.sin
		
		r0 = inner_radius
		r1 = outer_radius - tooth_depth/2.0
		r2 = outer_radius + tooth_depth/2.0
		
		da = 2.0*math.pi / teeth / 4.0
		
		GL.glShadeModel(GL.GL_FLAT)
		
		GL.glNormal3f(0.0, 0.0, 1.0)
		
		# draw front face 
		GL.glBegin(GL.GL_QUAD_STRIP)
		for i in range(teeth + 1):
			angle = i * 2.0*math.pi / teeth
			GL.glVertex3f(r0*cos(angle), r0*sin(angle), width*0.5)
			GL.glVertex3f(r1*cos(angle), r1*sin(angle), width*0.5)
			GL.glVertex3f(r0*cos(angle), r0*sin(angle), width*0.5)
			GL.glVertex3f(r1*cos(angle+3*da), r1*sin(angle+3*da), width*0.5)
		GL.glEnd()
		
		# draw front sides of teeth
		GL.glBegin(GL.GL_QUADS)
		da = 2.0*math.pi / teeth / 4.0
		for i in range(teeth):
			angle = i * 2.0*math.pi / teeth
			GL.glVertex3f(r1*cos(angle),			r1*sin(angle),			width*0.5)
			GL.glVertex3f(r2*cos(angle+da),		r2*sin(angle+da),		width*0.5)
			GL.glVertex3f(r2*cos(angle+2*da), r2*sin(angle+2*da), width*0.5)
			GL.glVertex3f(r1*cos(angle+3*da), r1*sin(angle+3*da), width*0.5)
		GL.glEnd()
		
		GL.glNormal3f(0.0, 0.0, -1.0)
		
		# draw back face
		GL.glBegin(GL.GL_QUAD_STRIP)
		for i in range(teeth + 1):
			angle = i * 2.0 * math.pi / teeth
			GL.glVertex3f(r1*cos(angle), r1*sin(angle), -width*0.5)
			GL.glVertex3f(r0*cos(angle), r0*sin(angle), -width*0.5)
			GL.glVertex3f(r1*cos(angle+3*da), r1*sin(angle+3*da),-width*0.5)
			GL.glVertex3f(r0*cos(angle), r0*sin(angle), -width*0.5)
		GL.glEnd()
		
		# draw back sides of teeth
		GL.glBegin(GL.GL_QUADS)
		da = 2.0*math.pi / teeth / 4.0
		for i in range(teeth):
			angle = i * 2.0*math.pi / teeth
			GL.glVertex3f(r1*cos(angle+3*da), r1*sin(angle+3*da),-width*0.5)
			GL.glVertex3f(r2*cos(angle+2*da), r2*sin(angle+2*da),-width*0.5)
			GL.glVertex3f(r2*cos(angle+da),		r2*sin(angle+da),	 -width*0.5)
			GL.glVertex3f(r1*cos(angle),			r1*sin(angle),		 -width*0.5)
		GL.glEnd()
		
		# draw outward faces of teeth
		GL.glBegin(GL.GL_QUAD_STRIP)
		for i in range(teeth):
			angle = i * 2.0*math.pi / teeth
			GL.glVertex3f(r1*cos(angle), r1*sin(angle),	 width*0.5)
			GL.glVertex3f(r1*cos(angle), r1*sin(angle), -width*0.5)
			u = r2*cos(angle+da) - r1*cos(angle)
			v = r2*sin(angle+da) - r1*sin(angle)
			len = math.sqrt(u*u + v*v)
			u = u / len
			v = v / len
			GL.glNormal3f(v, -u, 0.0)
			GL.glVertex3f(r2*cos(angle+da),		r2*sin(angle+da),		width*0.5)
			GL.glVertex3f(r2*cos(angle+da),		r2*sin(angle+da),	 -width*0.5)
			GL.glNormal3f(cos(angle), sin(angle), 0.0)
			GL.glVertex3f(r2*cos(angle+2*da), r2*sin(angle+2*da), width*0.5)
			GL.glVertex3f(r2*cos(angle+2*da), r2*sin(angle+2*da),-width*0.5)
			u = r1*cos(angle+3*da) - r2*cos(angle+2*da)
			v = r1*sin(angle+3*da) - r2*sin(angle+2*da)
			GL.glNormal3f(v, -u, 0.0)
			GL.glVertex3f(r1*cos(angle+3*da), r1*sin(angle+3*da), width*0.5)
			GL.glVertex3f(r1*cos(angle+3*da), r1*sin(angle+3*da),-width*0.5)
			GL.glNormal3f(cos(angle), sin(angle), 0.0)
		
		GL.glVertex3f(r1*cos(0), r1*sin(0), width*0.5)
		GL.glVertex3f(r1*cos(0), r1*sin(0), -width*0.5)
		
		GL.glEnd()
		
		GL.glShadeModel(GL.GL_SMOOTH)
		
		# draw inside radius cylinder
		GL.glBegin(GL.GL_QUAD_STRIP)
		for i in range(teeth + 1):
			angle = i * 2.0*math.pi / teeth;
			GL.glNormal3f(-cos(angle), -sin(angle), 0.0)
			GL.glVertex3f(r0*cos(angle), r0*sin(angle), -width*0.5)
			GL.glVertex3f(r0*cos(angle), r0*sin(angle), width*0.5)
		GL.glEnd()

#----------------------------------------------------------------------------

class GearsView(GLView):

	view_rotx=20.0
	view_roty=30.0
	view_rotz=0.0
	angle = 0.0

	def init_context(self):
		#print "Init Context" ###
		pos = (5.0, 5.0, 10.0, 0.0)
		red = (0.8, 0.1, 0.0, 1.0)
		green = (0.0, 0.8, 0.2, 1.0)
		blue = (0.2, 0.2, 1.0, 1.0)
		#
		GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, pos)
		GL.glEnable(GL.GL_CULL_FACE)
		GL.glEnable(GL.GL_LIGHTING)
		GL.glEnable(GL.GL_LIGHT0)
		GL.glEnable(GL.GL_DEPTH_TEST)
		#
		self.gear1 = GL.glGenLists(1)
		GL.glNewList(self.gear1, GL.GL_COMPILE)
		GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE, red)
		gear(1.0, 4.0, 1.0, 20, 0.7)
		GL.glEndList()
		#
		self.gear2 = GL.glGenLists(1)
		GL.glNewList(self.gear2, GL.GL_COMPILE)
		GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE, green)
		gear(0.5, 2.0, 2.0, 10, 0.7)
		GL.glEndList()
		#
		self.gear3 = GL.glGenLists(1)
		GL.glNewList(self.gear3, GL.GL_COMPILE)
		GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT_AND_DIFFUSE, blue)
		gear(1.3, 2.0, 0.5, 10, 0.7)
		GL.glEndList()
		#
		GL.glEnable(GL.GL_NORMALIZE)
		#
		self.frame_task = Task(self.next_frame, frame_interval, repeat = 1)

	def init_projection(self):
		#print "init_projection" ###
		width, height = self.size		 
		if width > height:
			w = float(width) / float(height)
			GL.glFrustum(-w, w, -1.0, 1.0, 5.0, 60.0)
		else:
			h = float(height) / float(width)
			GL.glFrustum(-1.0, 1.0, -h, h, 5.0, 60.0)

	def render(self):
		#print "Render" ###
		#GL.glMatrixMode(GL.GL_MODELVIEW)
		#GL.glLoadIdentity()
		GL.glTranslatef(0.0, 0.0, -40.0)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
		#
		GL.glPushMatrix()
		#
		GL.glRotatef(self.view_rotx, 1.0, 0.0, 0.0)
		GL.glRotatef(self.view_roty, 0.0, 1.0, 0.0)
		GL.glRotatef(self.view_rotz, 0.0, 0.0, 1.0)
		#
		GL.glPushMatrix()
		GL.glTranslatef(-3.0, -2.0, 0.0)
		GL.glRotatef(self.angle, 0.0, 0.0, 1.0)
		GL.glCallList(self.gear1)
		GL.glPopMatrix()
		#
		GL.glPushMatrix()
		GL.glTranslatef(3.1, -2.0, 0.0)
		GL.glRotatef(-2.0 * self.angle - 9.0, 0.0, 0.0, 1.0)
		GL.glCallList(self.gear2)
		GL.glPopMatrix()
		#
		GL.glPushMatrix()
		GL.glTranslatef(-3.1, 4.2, 0.0)
		GL.glRotatef(-2.0 * self.angle - 25.0, 0.0, 0.0, 1.0)
		GL.glCallList(self.gear3)
		GL.glPopMatrix()
		#
		GL.glPopMatrix()

	def next_frame(self):
		#print "Next Frame" ###
		self.angle += 2.0
		self.invalidate()
		self.update()
	
	def key_down(self, event):
		#print "Key:", event ###
		try:
			xa, ya, za = rotations[event.key]
			self.view_rotx += xa
			self.view_roty += ya
			self.view_rotz += za
		except KeyError:
			pass

#----------------------------------------------------------------------------

def test():
	view = GearsView(size = (300, 300))
	win = Window(title = "Gears")
	win.place(view, sticky = "nsew")
	view.become_target()
	win.shrink_wrap()
	win.show()
	application().run()

instructions = """
Gears should be spinning. The arrow keys should rotate the view.
"""

print instructions
test()
