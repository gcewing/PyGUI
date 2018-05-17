#
#   Python GUI - Drawing - Generic
#

from GUI.StdColors import black, white
from GUI.StdFonts import application_font
from GUI.Properties import Properties, overridable_property

class Canvas(Properties):

	_default_forecolor = black
	_default_backcolor = white
	_printing = False

	pencolor = overridable_property('pencolor', "Current color for stroking paths.")
	fillcolor = overridable_property('fillcolor', "Current color for filling paths.")
	textcolor = overridable_property('textcolor', "Current color for drawint text.")
	forecolor = overridable_property('forecolor', "Sets pen, fill and text colors to the same color.")
	backcolor = overridable_property('backcolor', "Current color for erasing regions.")
	pensize = overridable_property('pensize', "Width of pen for framing and stroking.")
	font = overridable_property('font', "Font for drawing text.")
	current_point = overridable_property('current_point', "The current point, or None.")
	printing = overridable_property('printing', "True if drawing destination is a non-display device.")

	#forecolor = overridable_property('forecolor', "Sets both pencolor and fillcolor.")

	def __init__(self):
		self.newpath()
	
	def get_printing(self):
		return self._printing

	def initgraphics(self):
		self.set_forecolor(self._default_forecolor)
		self.set_backcolor(self._default_backcolor)
		self.set_pensize(1)
		self.set_font(application_font)
	
	def set_forecolor(self, c):
		self.pencolor = c
		self.fillcolor = c
		self.textcolor = c
	
	def rmoveto(self, dx, dy):
		x0, y0 = self._current_point()
		self.moveto(x0 + dx, y0 + dy)
	
	def rlineto(self, dx, dy):
		x0, y0 = self.current_point
		self.lineto(x0 + dx, y0 + dy)
	
	def curve(self, sp, cp1, cp2, ep):
		self.moveto(sp)
		self.curveto(cp1, cp2, ep)
	
	def rcurveto(self, cp1, cp2, ep):
		x0, y0 = self.current_point
		x1, y1 = cp1
		x2, y2 = cp2
		x3, y3 = ep
		self.curveto(
			(x0 + x1, y0 + y1),
			(x0 + x2, y0 + y2),
			(x0 + x3, y0 + y3))
	
	def fill_stroke(self):
		self.fill()
		self.stroke()
	
	#  Rectangles
	
	def _pen_inset_rect(self, rect):
		l, t, r, b = rect
		p = 0.5 * self.pensize
		return (l + p, t + p, r - p, b - p)

	def rect(self, rect):
		l, t, r, b = rect
		self.moveto(l, t)
		self.lineto(r, t)
		self.lineto(r, b)
		self.lineto(l, b)
		self.closepath()
	
	def rect_frame(self, rect):
		self.rect(self._pen_inset_rect(rect))
	
	def fill_rect(self, rect):
		self.newpath()
		self.rect(rect)
		self.fill()
	
	def stroke_rect(self, rect):
		self.newpath()
		self.rect(rect)
		self.stroke()
	
	def frame_rect(self, rect):
		self.newpath()
		self.rect_frame(rect)
		self.stroke()

	def fill_stroke_rect(self, rect):
		self.rect_path(rect)
		self.fill_stroke()
	
	def fill_frame_rect(self, rect):
		self.fill_rect(rect)
		self.frame_rect(rect)
	
	def erase_rect(self, rect):
		self.newpath()
		self.rect(rect)
		self.erase()
	
	#  Ovals
	
	def oval_frame(self, rect):
		self.oval(self._pen_inset_rect(rect))
	
	def fill_oval(self, rect):
		self.newpath()
		self.oval_frame(rect)
		self.fill()
	
	def stroke_oval(self, rect):
		self.newpath()
		self.oval(rect)
		self.stroke()
	
	def frame_oval(self, rect):
		self.newpath()
		self.oval_frame(rect)
		self.stroke()

	def fill_stroke_oval(self, rect):
		self.newpath()
		self.oval(rect)
		self.fill_stroke()

	def fill_frame_oval(self, rect):
		self.fill_oval(rect)
		self.frame_oval()

	def erase_oval(self, rect):
		self.newpath()
		self.oval(rect)
		self.erase()
	
	#  Arcs
	
	def _arc_path(self, c, r, a0, a1):
#		x, y = c
#		a0r = a0 * deg
#		x0 = x + r * cos(a0r)
#		y0 = y + r * sin(a0r)
		self.newpath()
#		self.moveto(x0, y0)
		self.arc(c, r, a0, a1)
	
	def _arc_frame_path(self, c, r, a0, a1):
		self._arc_path(c, r - 0.5 * self.pensize, a0, a1)
	
	def stroke_arc(self, c, r, a0, a1):
		self._arc_path(c, r, a0, a1)
		self.stroke()
	
	def frame_arc(self, c, r, a0, a1):
		self._arc_frame_path(c, r, a0, a1)
		self.stroke()
	
		#  Wedges
	
	def wedge(self, c, r, a0, a1):
		self.moveto(*c)
		self.arc(c, r, a0, a1)
		self.closepath()
	
	def fill_wedge(self, c, r, a0, a1):
		self.newpath()
		self.wedge(c, r, a0, a1)
		self.fill()
	
	def stroke_wedge(self, c, r, a0, a1):
		self.newpath()
		self.wedge(c, r, a0, a1)
		self.stroke()
	
	def fill_stroke_wedge(self, c, r, a0, a1):
		self.newpath()
		self.wedge(c, r, a0, a1)
		self.fill_stroke()
	
	def erase_wedge(self, c, r, a0, a1):
		self.newpath()
		self.wedge(c, r, a0, a1)
		self.erase()
	
	#  Polylines
	
	def lines(self, points):
		point_iter = iter(points)
		self.moveto(*point_iter.next())
		for p in point_iter:
			self.lineto(*p)
	
	def linesto(self, points):
		for p in points:
			self.lineto(*p)
	
	def stroke_lines(self, points):
		self.newpath()
		self.lines(points)
		self.stroke()
	
	#  Polycurves
	
	def curves(self, points):
		self.moveto(*points[0])
		for i in xrange(1, len(points), 3):
			self.curveto(*points[i:i+3])
	
	def curvesto(self, points):
		for i in xrange(0, len(points), 3):
			self.curveto(*points[i:i+3])
				
	def stroke_curves(self, points):
		self.newpath()
		self.curves(points)
		self.stroke()
				
	#  Polygons

	def poly(self, points):
		self.lines(points)
		self.closepath()
		
	def fill_poly(self, points):
		self.newpath()
		self.poly(points)
		self.fill()
	
	def stroke_poly(self, points):
		self.newpath()
		self.poly(points)
		self.stroke()
	
	def fill_stroke_poly(self, points):
		self.newpath()
		self.poly(points)
		self.fill_stroke()

	def erase_poly(self, points):
		self.newpath()
		self.poly(points)
		self.erase()

	#  Loops
	
	def loop(self, points):
		self.curves(points)
		self.closepath()
	
	def fill_loop(self, points):
		self.newpath()
		self.loop(points)
		self.fill()
	
	def stroke_loop(self, points):
		self.newpath()
		self.loop(points)
		self.stroke()
	
	def fill_stroke_loop(self, points):
		self.newpath()
		self.loop(points)
		self.fill_stroke()

	def erase_loop(self, points):
		self.newpath()
		self.loop(points)
		self.erase()
