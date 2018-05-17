#--------------------------------------------------------------------
#
#   PyGUI - Canvas - Win32
#
#--------------------------------------------------------------------

from math import sin, cos, pi
import win32con as wc, win32ui as ui, win32gui as gui
from win32con import PS_SOLID, BS_SOLID, RGN_AND
#from win32ui import CreatePen, CreateBrush
#from win32gui import CloseFigure, PathToRegion, AngleArc
from GUI import export
import GUI.GDIPlus as gdip
from GUI.StdColors import black, white
from GUI.StdFonts import application_font
from GUI.WinUtils import win_null_brush
from GUI.GCanvases import Canvas as GCanvas

deg = pi / 180

def ir(x, i = int, r = round):
	return i(r(x))

def irr(rect, ir = ir):
	l, t, r, b = rect
	return (ir(l), ir(t), ir(r), ir(b))

#--------------------------------------------------------------------

class GState(object):

	pencolor = black
	fillcolor = black
	textcolor = black
	backcolor = white
	pensize = 1
	font = application_font
	
	win_pen = gdip.Pen(pencolor._win_argb, 1)
	win_fill_brush = gdip.SolidBrush(fillcolor._win_argb)
	win_text_brush = gdip.SolidBrush(textcolor._win_argb)
	win_bg_brush = gdip.SolidBrush(backcolor._win_argb)
	
	def __init__(self, clone = None):
		if clone:
			self.__dict__.update(clone.__dict__)

#--------------------------------------------------------------------

class Canvas(GCanvas):

	_current_point = None
	
#	def __init__(self, win_graphics, dc = None):
#		if not dc:
#			print "Canvas.__init__: before get dc: clip bounds =", win_graphics.GetClipBounds() ###
#			dc = ui.CreateDCFromHandle(win_graphics.GetHDC())
#			print "Canvas.__init__: after get dc: clip bounds =", win_graphics.GetClipBounds() ###
#		dc.SetBkMode(wc.TRANSPARENT)
#		dc.SetTextAlign(wc.TA_LEFT | wc.TA_BASELINE | wc.TA_UPDATECP)
#		print "Canvas.__init__: clip bounds =", win_graphics.GetClipBounds() ###
#		self._win_graphics = win_graphics
#		self._win_dc = dc
#		self._win_hdc = dc.GetHandleOutput()
#		self._win_path = gdip.GraphicsPath()
#		self._state = GState()
#		self._stack = []
	
	def __init__(self, win_graphics, for_printing = False):
		self._win_graphics = win_graphics
		self._win_path = gdip.GraphicsPath()
		self._state = GState()
		self._stack = []
		if for_printing:
			unit = gdip.UnitPoint
			win_graphics.SetPageUnit(unit)
		#else:
		#	unit = gdip.UnitPixel
		
#		dpix = win_graphics.GetDpiX()
#		dpiy = win_graphics.GetDpiY()
#		print "Canvas: dpi =", dpix, dpiy ###
#		win_graphics.SetPageUnit(gdip.UnitPoint)
#		if not for_printing:
#			sx = 72.0 / dpix
#			sy = 72.0 / dpiy
#			self.scale(sx, sy)

	def _from_win_dc(cls, dc):
		return cls._from_win_hdc(dc.GetSafeHdc())
	
	_from_win_dc = classmethod(_from_win_dc)

	def _from_win_hdc(cls, hdc, **kwds):
		win_graphics = gdip.Graphics.from_hdc(hdc)
		return cls(win_graphics, **kwds)
	
	_from_win_hdc = classmethod(_from_win_hdc)
	
	def _from_win_image(cls, win_image):
		win_graphics = gdip.Graphics.from_image(win_image)
		#print "Canvas._from_win_image: win_graphics =", win_graphics ###
		#print "... clip bounds =", win_graphics.GetClipBounds() ###
		return cls(win_graphics)
	
	_from_win_image = classmethod(_from_win_image)

	def get_pencolor(self):
		return self._state.pencolor
	
	def set_pencolor(self, c):
		state = self._state
		state.pencolor = c
		state.win_pen = gdip.Pen(c._win_argb, state.pensize)
	
	def get_fillcolor(self):
		return self._state.fillcolor
	
	def set_fillcolor(self, c):
		state = self._state
		state.fillcolor = c
		state.win_fill_brush = gdip.SolidBrush(c._win_argb)
	
	def get_textcolor(self):
		return self._state.textcolor
	
	def set_textcolor(self, c):
		state = self._state
		state.textcolor = c
		state.win_text_brush = gdip.SolidBrush(c._win_argb)
	
	def get_backcolor(self):
		return self._state.backcolor
	
	def set_backcolor(self, c):
		state = self._state
		state.backcolor = c
		state.win_bg_brush = gdip.SolidBrush(c._win_argb)
	
	def get_pensize(self):
		return self._state.pensize
	
	def set_pensize(self, x):
		state = self._state
		state.pensize = x
		state.win_pen = gdip.Pen(state.pencolor._win_argb, x)
	
	def get_current_point(self):
		return self._current_point
	
	def get_font(self):
		return self._state.font
	
	def set_font(self, f):
		self._state.font = f

	def newpath(self):
		self._win_path.Reset()
	
	def moveto(self, x, y):
		p = (x, y)
		self._current_point = p
		self._win_path.StartFigure()
	
	def lineto(self, x, y):
		x0, y0 = self._current_point
		self._win_path.AddLine_4f(x0, y0, x, y)
		self._current_point = (x, y)
	
	def curveto(self, p1, p2, p3):
		p0 = self._current_point
		self._win_path.AddBezier_4p(p0, p1, p2, p3)
		self._current_point = p3
	
	def arc(self, c, r, a0, a1):
		g = self._win_path
		g.AddArc_p3f(c, r, a0, a1)
		self._current_point = g.GetLastPoint()
	
	def closepath(self):
		self._win_path.CloseFigure()
		self._current_point = None
	
	def fill(self):
		self._win_graphics.FillPath(self._state.win_fill_brush, self._win_path)
	
	def stroke(self):
		self._win_graphics.DrawPath(self._state.win_pen, self._win_path)
	
	def erase(self):
		g = self._win_graphics
		g.SetSourceCopyMode()
		g.FillPath(self._state.win_bg_brush, self._win_path)
		g.SetSourceOverMode()

	def show_text(self, text):
		font = self._state.font
		gf = font._win_gdip_font
		x, y = self._current_point
		brush = self._state.win_text_brush
		g = self._win_graphics
		w = g.DrawAndMeasureStringWidth_2f(text, gf, x, y, brush)
		self._current_point = x + w, y
	
##
##   GDI+ screws up some fonts (e.g. Times) for some reason.
##   Using plain GDI to draw text for now.
##
#	def show_text(self, text):
#		state = self._state
#		x, y = self._current_point
#		dc = self._win_dc
#		dc.SelectObject(state.font._win_font)
#		dc.SetTextColor(state.textcolor._win_color)
#		dc.MoveTo(ir(x), ir(y))
#		dc.TextOut(20, 20, text)
#		self._current_point = dc.GetCurrentPosition()

	def clip(self):
		self._win_graphics.SetClip_PI(self._win_path)

	def rectclip(self, rect):
		self._win_graphics.SetClip_rI(rect)

	def gsave(self):
		old_state = self._state
		old_state.win_state = self._win_graphics.Save()
		self._stack.append(old_state)
		self._state = GState(old_state)
	
	def grestore(self):
		old_state = self._stack.pop()
		self._win_graphics.Restore(old_state.win_state)
		self._state = old_state
	
	#  Rectangles

	def rect(self, rect):
		self._win_path.AddRectangle_r(rect)
		self._current_point = None
	
	def fill_rect(self, rect):
		self._win_graphics.FillRectangle_r(self._state.win_fill_brush, rect)
	
	def stroke_rect(self, rect):
		self._win_graphics.DrawRectangle_r(self._state.win_pen, rect)
	
	def erase_rect(self, rect):
		self._win_graphics.FillRectangle_r(self._state.win_bg_brush, rect)
	
	#  Ovals
	
	def oval(self, rect):
		self._win_path.AddEllipse_r(rect)
		self._current_point = None
	
	def fill_oval(self, rect):
		self._win_graphics.FillEllipse_r(self._state.win_fill_brush, rect)
	
	def stroke_oval(self, rect):
		self._win_graphics.DrawEllipse_r(self._state.win_pen, rect)
	
	def erase_oval(self, rect):
		self._win_graphics.FillEllipse_r(self._state.win_bg_brush, rect)
	
	#  Arcs
	
	def stroke_arc(self, c, r, a0, a1):
		self._win_graphics.DrawArc_3pf(self._state.win_pen, c, r, a0, a1)
	
	#  Wedges
	
	def wedge(self, c, r, a0, a1):
		self._win_path.AddPie_p3f(c, r, a0, a1)
		self._current_point = None
	
	def stroke_wedge(self, c, r, a0, a1):
		self._win_graphics.DrawPie_p3f(self._state.win_pen, c, r, a0, a1)
	
	def fill_wedge(self, c, r, a0, a1):
		self._win_graphics.FillPie_p3f(self._state.win_fill_brush, c, r, a0, a1)
	
	def erase_wedge(self, c, r, a0, a1):
		self._win_graphics.FillPie_p3f(self._state.win_bg_brush, c, r, a0, a1)
	
	#  Polylines
	
	def lines(self, points):
		self._win_path.AddLines_pv(points)
		self._current_point = points[-1]
	
	def linesto(self, points):
		self.lines([self._current_point] + points)

	def stroke_lines(self, points):
		self._win_graphics.DrawLines_pv(self._state.win_pen, points)

	#  Polygons

	def poly(self, points):
		self._win_path.AddPolygon_pv(points)
		self._current_point = None

	def stroke_poly(self, points):
		self._win_graphics.DrawPolygon_pv(self._state.win_pen, points)

	def fill_poly(self, points):
		self._win_graphics.FillPolygon_pv(self._state.win_fill_brush, points)

	def erase_poly(self, points):
		self._win_graphics.FillPolygon_pv(self._state.win_bg_brush, points)

	#  Polycurves
	
	def curves(self, points):
		self._win_path.AddBeziers_pv(points)
		self._current_point = points[-1]
	
	def curvesto(self, points):
		self.curves([self._current_point] + points)
	
	def stroke_curves(self, points):
		self._win_graphics.DrawBeziers_pv(self._state.win_pen, points)

	#  Transformations
	
	def translate(self, dx, dy):
		self._win_graphics.Translate_2f(dx, dy)

	def scale(self, sx, sy):
		self._win_graphics.Scale_2f(sx, sy)

export(Canvas)
