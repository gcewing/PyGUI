#
#   Python GUI - Drawing - PyObjC
#

from array import array
from Foundation import NSPoint, NSMakeRect, NSString
from AppKit import NSGraphicsContext, NSBezierPath, NSEvenOddWindingRule, \
	NSFontAttributeName, NSForegroundColorAttributeName, \
	NSCompositeCopy, NSCompositeSourceOver
from GUI import export
from GUI.StdColors import black, white
from GUI.GCanvases import Canvas as GCanvas

class Canvas(GCanvas):

	def __init__(self):
		self._ns_path = NSBezierPath.bezierPath()
		self._ns_path.setWindingRule_(NSEvenOddWindingRule)
		self._stack = []
		ctx = NSGraphicsContext.currentContext()
		ctx.setCompositingOperation_(NSCompositeSourceOver)
		GCanvas.__init__(self)
		self._printing = not ctx.isDrawingToScreen()
		self.initgraphics()
	
	def get_pencolor(self):
		return self._pencolor
	
	def set_pencolor(self, c):
		self._pencolor = c
	
	def get_fillcolor(self):
		return self._fillcolor
	
	def set_fillcolor(self, c):
		self._fillcolor = c
	
	def get_textcolor(self):
		return self._textcolor
	
	def set_textcolor(self, c):
		self._textcolor = c
	
	def get_backcolor(self):
		return self._backcolor
	
	def set_backcolor(self, c):
		self._backcolor = c
	
	def get_pensize(self):
		return self._pensize
	
	def set_pensize(self, d):
		self._pensize = d
		self._ns_path.setLineWidth_(d)
	
	def get_font(self):
		return self._font
	
	def set_font(self, f):
		self._font = f
	
	def get_current_point(self):
		return self._ns_path.currentPoint()
	
	def newpath(self):
		self._ns_path.removeAllPoints()
	
	def moveto(self, x, y):
		self._ns_path.moveToPoint_((x, y))
	
	def rmoveto(self, dx, dy):
		self._ns_path.relativeMoveToPoint_((dx, dy))

	def lineto(self, x, y):
		self._ns_path.lineToPoint_((x, y))

	def rlineto(self, dx, dy):
		self._ns_path.relativeLineToPoint_((dx, dy))
	
	def curveto(self, cp1, cp2, ep):
		self._ns_path.curveToPoint_controlPoint1_controlPoint2_(
			ep, cp1, *cp2)
	
	def rcurveto(self, cp1, cp2, ep):
		self._ns_path.relativeCurveToPoint_controlPoint1_controlPoint2_(
			ep, cp1, cp2)
	
	def arc(self, c, r, a0, a1):
		self._ns_path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_(
			c, r, a0, a1)
	
	def rect(self, rect):
		self._ns_path.appendBezierPathWithRect_(_ns_rect(rect))
	
	def oval(self, rect):
		self._ns_path.appendBezierPathWithOvalInRect(_ns_rect(rect))
	
	def lines(self, points):
		#  Due to a memory leak in PyObjC 2.3, we need to be very careful
		#  about the type of object that we pass to appendBezierPathWithPoints_count_.
		#  If 'points' is a numpy array, we convert it to an array.array of type 'f',
		#  else we fall back on iterating over the points in Python.
#		ns = self._ns_path
#		ns.moveToPoint_(points[0])
#		ns.appendBezierPathWithPoints_count_(points, len(points))
		try:
			p = points.flat
		except AttributeError:
			GCanvas.lines(self, points)
		else:
			a = array('f', p)
			ns = self._ns_path
			ns.moveToPoint_(points[0])
			ns.appendBezierPathWithPoints_count_(a, len(points))
			
	
	def poly(self, points):
#		ns = self._ns_path
#		ns.moveToPoint_(points[0])
#		ns.appendBezierPathWithPoints_count_(points, len(points))
#		ns.closePath()
		self.lines(points)
		self.closepath()

	def closepath(self):
		self._ns_path.closePath()

	def clip(self):
		ns = self._ns_path
		ns.addClip()

	def rectclip(self, (l, t, r, b)):
		ns_rect = NSMakeRect(l, t, r - l, b - t)
		NSBezierPath.clipRect_(ns_rect)

	def gsave(self):
		self._stack.append((
			self._pencolor, self._fillcolor, self._textcolor, self._backcolor,
			self._pensize, self._font))
		NSGraphicsContext.currentContext().saveGraphicsState()
	
	def grestore(self):
		(self._pencolor, self._fillcolor, self._textcolor, self._backcolor,
			self._pensize, self._font) = self._stack.pop()
		NSGraphicsContext.currentContext().restoreGraphicsState()
	
	def stroke(self):
		ns = self._ns_path
		self._pencolor._ns_color.set()
		ns.stroke()

	def fill(self):
		ns = self._ns_path
		self._fillcolor._ns_color.set()
		ns.fill()
	
	def erase(self):
		ns = self._ns_path
		self._backcolor._ns_color.set()
		ctx = NSGraphicsContext.currentContext()
		ctx.setCompositingOperation_(NSCompositeCopy)
		ns.fill()
		ctx.setCompositingOperation_(NSCompositeSourceOver)
	
	def fill_stroke(self):
		ns = self._ns_path
		self._pencolor._ns_color.set()
		ns.stroke()
		self._fillcolor._ns_color.set()
		ns.fill()
	
	def show_text(self, text):
		x, y = self._ns_path.currentPoint()
		font = self._font
		ns_font = font._ns_font
		ns_color = self._textcolor._ns_color
		ns_string = NSString.stringWithString_(text)
		ns_attrs = {
			NSFontAttributeName: ns_font,
			NSForegroundColorAttributeName: ns_color,
		}
#		print "Canvas.show_text:", repr(text) ###
#		print "family:", ns_font.familyName() ###
#		print "size:", ns_font.pointSize() ###
#		print "ascender:", ns_font.ascender() ###
#		print "descender:", ns_font.descender() ###
#		print "capHeight:", ns_font.capHeight() ###
#		print "leading:", ns_font.leading() ###
#		print "matrix:", ns_font.matrix() ###
#		print "defaultLineHeightForFont:", ns_font.defaultLineHeightForFont() ###
		h = ns_font.defaultLineHeightForFont()
		d = -ns_font.descender()
		dy = h - d
		if ns_font.familyName() == "Courier New":
			dy += ns_font.pointSize() * 0.229167
		ns_point = NSPoint(x, y - dy)
		#print "drawing at:", ns_point ###
		ns_string.drawAtPoint_withAttributes_(ns_point, ns_attrs)
		dx = ns_font.widthOfString_(ns_string)
		#self._ns_path.relativeMoveToPoint_(NSPoint(x + dx, y))
		self._ns_path.relativeMoveToPoint_((dx, 0))
	
	def _ns_frame_rect(self, (l, t, r, b)):
		p = self._pensize
		q = 0.5 * p
		return NSMakeRect(l + q, t + q, r - l - p, b - t - p)

	def stroke_rect(self, r):
		self._pencolor._ns_color.set()
		NSBezierPath.setDefaultLineWidth_(self._pensize)
		NSBezierPath.strokeRect_(_ns_rect(r))

	def frame_rect(self, r):
		self._pencolor._ns_color.set()
		NSBezierPath.setDefaultLineWidth_(self._pensize)
		NSBezierPath.strokeRect_(self._ns_frame_rect(r))
	
	def fill_rect(self, r):
		self._fillcolor._ns_color.set()
		NSBezierPath.fillRect_(_ns_rect(r))
	
	def erase_rect(self, r):
		self._backcolor._ns_color.set()
		NSBezierPath.fillRect_(_ns_rect(r))
	
	def _ns_oval_path(self, ns_rect):
		ns_path = NSBezierPath.bezierPathWithOvalInRect_(ns_rect)
		ns_path.setLineWidth_(self._pensize)
		return ns_path
	
	def stroke_oval(self, r):
		self._pencolor._ns_color.set()
		self._ns_oval_path(_ns_rect(r)).stroke()
	
	def frame_oval(self, r):
		self._pencolor._ns_color.set()
		self._ns_oval_path(self._ns_frame_rect(r)).stroke()
	
	def fill_oval(self, r):
		self._fillcolor._ns_color.set()
		self._ns_oval_path(_ns_rect(r)).fill()
	
	def erase_oval(self, r):
		self._backcolor._ns_color.set()
		self._ns_oval_path(_ns_rect(r)).fill()
	
	def _ns_arc_path(self, c, r, sa, ea):
		ns_path = NSBezierPath.bezierPath()
		ns_path.setLineWidth_(self._pensize)
		ns_path.\
			appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_(
				c, r, sa, ea)
		return ns_path
	
	def stroke_arc(self, center, radius, start_angle, arc_angle):
		ns_path = self._ns_arc_path(center, radius, start_angle, arc_angle)
		self._pencolor._ns_color.set()
		ns_path.stroke()
	
	def frame_arc(self, center, radius, start_angle, arc_angle):
		r = radius - 0.5 * self._pensize
		ns_path = self._ns_arc_path(center, r, start_angle, arc_angle)
		self._pencolor._ns_color.set()
		ns_path.stroke()

def _ns_rect((l, t, r, b)):
	return NSMakeRect(l, t, r - l, b - t)

export(Canvas)

