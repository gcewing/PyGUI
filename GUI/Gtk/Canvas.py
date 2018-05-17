#--------------------------------------------------------------------
#
#   Python GUI - Canvas - Gtk
#
#--------------------------------------------------------------------

from math import sin, cos, pi, floor
from cairo import OPERATOR_OVER, OPERATOR_SOURCE, FILL_RULE_EVEN_ODD
from GUI import export
from GUI.Geometry import sect_rect
from GUI.StdFonts import application_font
from GUI.StdColors import black, white
from GUI.GCanvases import Canvas as GCanvas
from GUI.GCanvasPaths import CanvasPaths as GCanvasPaths

deg = pi / 180
twopi = 2 * pi

#--------------------------------------------------------------------

class GState(object):

	pencolor = black
	fillcolor = black
	textcolor = black
	backcolor = white
	pensize = 1
	font = application_font
	
	def __init__(self, clone = None):
		if clone:
			self.__dict__.update(clone.__dict__)

#--------------------------------------------------------------------

class Canvas(GCanvas, GCanvasPaths):

	def _from_gdk_drawable(cls, gdk_drawable):
		return cls(gdk_drawable.cairo_create())
	
	_from_gdk_drawable = classmethod(_from_gdk_drawable)
	
	def _from_cairo_context(cls, ctx):
		return cls(ctx)
	
	_from_cairo_context = classmethod(_from_cairo_context)

	def __init__(self, ctx):
		ctx.set_fill_rule(FILL_RULE_EVEN_ODD)
		self._gtk_ctx = ctx
		self._gstack = []
		self._state = GState()
		GCanvas.__init__(self)
		GCanvasPaths.__init__(self)
	
	def get_pencolor(self):
		return self._state.pencolor
	
	def set_pencolor(self, c):
		self._state.pencolor = c
	
	def get_fillcolor(self):
		return self._state.fillcolor
	
	def set_fillcolor(self, c):
		self._state.fillcolor = c
	
	def get_textcolor(self):
		return self._state.textcolor
	
	def set_textcolor(self, c):
		self._state.textcolor = c
	
	def get_backcolor(self):
		return self._state.backcolor
	
	def set_backcolor(self, c):
		self._state.backcolor = c
	
	def get_pensize(self):
		return self._state.pensize
	
	def set_pensize(self, d):
		self._state.pensize = d
	
	def get_font(self):
		return self._state.font
	
	def set_font(self, f):
		self._state.font = f
	
	def get_current_point(self):
		return self._gtk_ctx.get_current_point()
	
	def rectclip(self, r):
		l, t, r, b = r
		ctx = self._gtk_ctx
		ctx.new_path()
		ctx.rectangle(l, t, r - l, b - t)
		ctx.clip()
	
	def gsave(self):
		old_state = self._state
		self._gstack.append(old_state)
		self._state = GState(old_state)
		self._gtk_ctx.save()
	
	def grestore(self):
		self._state = self._gstack.pop()
		self._gtk_ctx.restore()
	
	def newpath(self):
		self._gtk_ctx.new_path()
	
	def moveto(self, x, y):
		self._gtk_ctx.move_to(x, y)
	
	def rmoveto(self, x, y):
		self._gtk_ctx.rel_move_to(x, y)
	
	def lineto(self, x, y):
		self._gtk_ctx.line_to(x, y)
	
	def rlineto(self, x, y):
		self._gtk_ctx.rel_line_to(x, y)
	
	def curveto(self, p1, p2, p3):
		self._gtk_ctx.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
	
	def rcurveto(self, p1, p2, p3):
		self._gtk_ctx.rel_curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
	
	def arc(self, c, r, a0, a1):
		self._gtk_ctx.arc(c[0], c[1], r, a0 * deg, a1 * deg)
	
	def closepath(self):
		ctx = self._gtk_ctx
		ctx.close_path()
		ctx.new_sub_path()
	
	def clip(self):
		self._gtk_ctx.clip_preserve()
	
	def stroke(self):
		state = self._state
		ctx = self._gtk_ctx
		#ctx.set_source_rgba(*state.pencolor._rgba)
		ctx.set_source_color(state.pencolor._gdk_color)
		ctx.set_line_width(state.pensize)
		ctx.stroke_preserve()
	
	def fill(self):
		ctx = self._gtk_ctx
		#ctx.set_source_rgba(*self._state.fillcolor._rgba)
		ctx.set_source_color(self._state.fillcolor._gdk_color)
		ctx.fill_preserve()
	
	def erase(self):
		ctx = self._gtk_ctx
		#ctx.set_source_rgba(*self._state.backcolor._rgba)
		ctx.set_source_color(self._state.backcolor._gdk_color)
		ctx.set_operator(OPERATOR_SOURCE)
		ctx.fill_preserve()
		ctx.set_operator(OPERATOR_OVER)

	def show_text(self, text):
		font = self._state.font
		layout = font._get_pango_layout(text, True)
		dx = layout.get_pixel_size()[0]
		dy = font.ascent
		ctx = self._gtk_ctx
		#ctx.set_source_rgba(*self._state.textcolor._rgba)
		ctx.set_source_color(self._state.textcolor._gdk_color)
		ctx.rel_move_to(0, -dy)
		ctx.show_layout(layout)
		ctx.rel_move_to(dx, dy)

	def rect(self, rect):
		l, t, r, b = rect
		self._gtk_ctx.rectangle(l, t, r - l, b - t)
	
	def oval(self, rect):
		l, t, r, b = rect
		a = 0.5 * (r - l)
		b = 0.5 * (b - t)
		ctx = self._gtk_ctx
		ctx.new_sub_path()
		ctx.save()
		ctx.translate(l + a, t + b)
		ctx.scale(a, b)
		ctx.arc(0, 0, 1, 0, twopi)
		ctx.close_path()
		ctx.restore()
	
	def translate(self, dx, dy):
		self._gtk_ctx.translate(dx, dy)

#	def _coords(self, x, y):
#		x0, y0 = self._origin
#		return int(round(x0 + x)), int(round(y0 + y))

#	def _coords(self, x, y):
#		return int(round(x)), int(round(y))

#	def _rect_coords(self, (l, t, r, b)):
#		x0, y0 = self._origin
#		l = int(round(x0 + l))
#		t = int(round(y0 + t))
#		r = int(round(x0 + r))
#		b = int(round(y0 + b))
#		return l, t, r - l, b - t
	
#	def _rect_coords(self, (l, t, r, b)):
#		l = int(round(l))
#		t = int(round(t))
#		r = int(round(r))
#		b = int(round(b))
#		return l, t, r - l, b - t

#	def _frame_coords(self, r):
#		l, t, w, h = self._rect_coords(r)
#		p = self._gdk_gc.line_width
#		d = p // 2
#		return (
#			int(floor(l + d)),
#			int(floor(t + d)),
#			int(floor(w - p)),
#			int(floor(h - p)))

#def _gdk_angles(start_angle, end_angle):
#	arc_angle = (end_angle - start_angle) % 360
#	start = int(round(start_angle * 64))
#	arc = int(round((arc_angle) * 64))
#	return -start, -arc

#def _arc_rect((cx, cy), r):
#	return (cx - r, cy - r, cx + r, cy + r)

#def _arc_endpoint(center, r, a):
#	cx, cy = center
#	ar = a * deg
#	x = int(round(cx + r * cos(ar)))
#	y = int(round(cy + r * sin(ar)))
#	return x, y

export(Canvas)
