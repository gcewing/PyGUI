#--------------------------------------------------------------------
#
#   PyGUI - Win32 - GDI Plus
#
#--------------------------------------------------------------------

from ctypes import *
from ctypes.wintypes import BOOL
try:
	from numpy import ndarray, float32
except ImportError:
	class ndarray(object):
		pass

#wg = windll.gdiplus
wg = oledll.gdiplus

#--------------------------------------------------------------------

# enum Unit

UnitWorld = 0
UnitDisplay = 1
UnitPixel = 2
UnitPoint = 3

# enum FillMode

FillModeAlternate = 0

# enum CombineMode

CombineModeIntersect = 1

# enum MatrixOrder

MatrixOrderPrepend = 0
MatrixOrderAppend = 1

# Pixel Formats

# In-memory pixel data formats:
# bits 0-7 = format index
# bits 8-15 = pixel size (in bits)
# bits 16-23 = flags
# bits 24-31 = reserved

PixelFormatIndexed     = 0x00010000 # Indexes into a palette
PixelFormatGDI         = 0x00020000 # Is a GDI-supported format
PixelFormatAlpha       = 0x00040000 # Has an alpha component
PixelFormatPAlpha      = 0x00080000 # Pre-multiplied alpha
PixelFormatExtended    = 0x00100000 # Extended color 16 bits/channel
PixelFormatCanonical   = 0x00200000 

PixelFormat1bppIndexed    = (1 | ( 1 << 8) | PixelFormatIndexed | PixelFormatGDI)
PixelFormat4bppIndexed    = (2 | ( 4 << 8) | PixelFormatIndexed | PixelFormatGDI)
PixelFormat8bppIndexed    = (3 | ( 8 << 8) | PixelFormatIndexed | PixelFormatGDI)
PixelFormat16bppGrayScale = (4 | (16 << 8) | PixelFormatExtended)
PixelFormat16bppRGB555    = (5 | (16 << 8) | PixelFormatGDI)
PixelFormat16bppRGB565    = (6 | (16 << 8) | PixelFormatGDI)
PixelFormat16bppARGB1555  = (7 | (16 << 8) | PixelFormatAlpha | PixelFormatGDI)
PixelFormat24bppRGB       = (8 | (24 << 8) | PixelFormatGDI)
PixelFormat32bppRGB       = (9 | (32 << 8) | PixelFormatGDI)
PixelFormat32bppARGB      = (10 | (32 << 8) | PixelFormatAlpha | PixelFormatGDI | PixelFormatCanonical)
PixelFormat32bppPARGB     = (11 | (32 << 8) | PixelFormatAlpha | PixelFormatPAlpha | PixelFormatGDI)
PixelFormat48bppRGB       = (12 | (48 << 8) | PixelFormatExtended)
PixelFormat64bppARGB      = (13 | (64 << 8) | PixelFormatAlpha  | PixelFormatCanonical | PixelFormatExtended)
PixelFormat64bppPARGB     = (14 | (64 << 8) | PixelFormatAlpha  | PixelFormatPAlpha | PixelFormatExtended)

# enum FontStyle

FontStyleBold = 1
FontStyleItalic = 2
FontStyleUnderline = 4
FontStyleStrikeout = 8

class PointF(Structure):
	_fields_ = [("x", c_float), ("y", c_float)]

class RectF(Structure):
	_fields_ = [
		("x", c_float), ("y", c_float),
		("width", c_float), ("height", c_float)]

#--------------------------------------------------------------------

def rect_args(rect):
	l, t, r, b = rect
	return c_float(l), c_float(t), c_float(r - l), c_float(b -  t)

def points_args(points):
	if isinstance(points, ndarray) and points.flags['C_CONTIGUOUS'] and points.dtype == float32:
		#print "GDIPlus.points_args: using ndarray" ###
		n = points.size // 2
		buf = points.ctypes.data
	else:
		n = len(points)
		buf = (PointF * n)()
		for i, p in enumerate(points):
			buf[i].x, buf[i].y = p
	return buf, n

def arc_args(c, r, a0, a1):
	x, y = c
	d = c_float(2 * r)
	return c_float(x - r), c_float(y - r), d, d, \
		c_float(a0), c_float((a1 - a0) % 360.0)

#--------------------------------------------------------------------

class GdiplusStartupInput(Structure):

	_fields_ = [
		('GdiplusVersion', c_uint),
		('DebugEventCallback', c_void_p),
		('SuppressBackgroundThread', BOOL),
		('SuppressExternalCodecs', BOOL),
	]

	def __init__(self):
		Structure.__init__(self)
		self.GdiplusVersion = 1
		self.DebugEventCallback = None
		self.SuppressBackgroundThread = 0
		self.SuppressExternalCodecs = 0

StartupInput = GdiplusStartupInput()
token = c_ulong()
wg.GdiplusStartup(pointer(token), pointer(StartupInput), None)

#--------------------------------------------------------------------

class Pen(object):

	def __init__(self, argb, size):
		ptr = c_void_p()
		wg.GdipCreatePen1(argb, c_float(size), UnitWorld, byref(ptr))
		self.ptr = ptr
	
	def __del__(self, wg = wg):
		wg.GdipDeletePen(self.ptr)

#--------------------------------------------------------------------

class SolidBrush(object):

	def __init__(self, argb):
		ptr = c_void_p()
		wg.GdipCreateSolidFill(argb, byref(ptr))
		self.ptr = ptr
	
	def __del__(self, wg = wg):
		wg.GdipDeleteBrush(self.ptr)
	
	def __str__(self):
		argb = c_ulong()
		wg.GdipGetSolidFillColor(self.ptr, byref(argb))
		return "<SolidBrush argb=0x%08x>" % argb.value

#--------------------------------------------------------------------

class Font(object):

	def __init__(self, family, size, style):
		uname = create_unicode_buffer(family)
		fam = c_void_p()
		wg.GdipCreateFontFamilyFromName(uname, None, byref(fam))
		flags = 0
		if 'bold' in style:
			flags |= FontStyleBold
		if 'italic' in style:
			flags |= FontStyleItalic
		ptr = c_void_p()
		wg.GdipCreateFont(fam, c_float(size), flags, UnitWorld, byref(ptr))
		self.ptr = ptr
		wg.GdipDeleteFontFamily(fam)

	def from_hdc(cls, hdc):
		self = cls.__new__(cls)
		ptr = c_void_p()
		wg.GdipCreateFontFromDC(hdc, byref(ptr))
		self.ptr = ptr
		return self
	
	from_hdc = classmethod(from_hdc)
		
	def __del__(self, wg = wg):
		wg.GdipDeleteFont(self.ptr)

#--------------------------------------------------------------------

class Image(object):

	def __str__(self):
		return "<Image 0x%x>" % self.ptr.value

	def from_file(cls, path):
		self = cls.__new__(cls)
		ptr = c_void_p()
		upath = create_unicode_buffer(path)
		self._create_from_file(upath, ptr)
		self.ptr = ptr
		return self
	
	from_file = classmethod(from_file)
	
	def _create_from_file(self, upath, ptr):
		wg.GdipLoadImageFromFile(upath, byref(ptr))

	def __del__(self, wg = wg):
		wg.GdipDisposeImage(self.ptr)

	def GetWidth(self):
		uint = c_uint()
		wg.GdipGetImageWidth(self.ptr, byref(uint))
		return uint.value

	def GetHeight(self):
		uint = c_uint()
		wg.GdipGetImageHeight(self.ptr, byref(uint))
		return uint.value

#--------------------------------------------------------------------

class Bitmap(Image):

	def __init__(self, width, height):
		ptr = c_void_p()
		format = PixelFormat32bppARGB
		wg.GdipCreateBitmapFromScan0(width, height, 0, format, None, byref(ptr))
		self.ptr = ptr
		#print "GDIPlus.Bitmap:", (width, height), repr(self), "ptr =", self.ptr ###

	def _create_from_file(self, upath, ptr):
		wg.GdipCreateBitmapFromFile(upath, byref(ptr))
	
	def from_data(cls, width, height, format, data):
		self = cls.__new__(cls)
		ptr = c_void_p()
		bits_per_pixel = (format >> 8) & 0xff
		row_stride = (width * bits_per_pixel) >> 3
		wg.GdipCreateBitmapFromScan0(width, height, row_stride, format, data, byref(ptr))
		self.ptr = ptr
		return self
	
	from_data = classmethod(from_data)
	
	def __str__(self):
		return "<Bitmap 0x%x>" % self.ptr.value

	def GetHICON(self):
		hicon = c_ulong()
		wg.GdipCreateHICONFromBitmap(self.ptr, byref(hicon))
		return hicon.value
	
	def GetPixel(self, x, y):
		c = c_ulong()
		wg.GdipBitmapGetPixel(self.ptr, x, y, byref(c))
		return c.value
	
	def SetPixel(self, x, y, c):
		wg.GdipBitmapSetPixel(self.ptr, x, y, c)

#--------------------------------------------------------------------

class GraphicsPath(object):

	def __init__(self):
		ptr = c_void_p()
		wg.GdipCreatePath(FillModeAlternate, byref(ptr))
		self.ptr = ptr
	
	def __del__(self, wg = wg):
		wg.GdipDeletePath(self.ptr)
	
	def Reset(self):
		wg.GdipResetPath(self.ptr)

	def StartFigure(self):
		wg.GdipStartPathFigure(self.ptr)

	def AddLine_4f(self, x0, y0, x1, y1):
		wg.GdipAddPathLine(self.ptr,
			c_float(x0), c_float(y0), c_float(x1), c_float(y1))
	
	def AddBezier_4p(self, p0, p1, p2, p3):
		x0, y0 = p0
		x1, y1 = p1
		x2, y2 = p2
		x3, y3 = p3
		wg.GdipAddPathBezier(self.ptr,
			c_float(x0), c_float(y0), c_float(x1), c_float(y1),
			c_float(x2), c_float(y2), c_float(x3), c_float(y3))
	
	def AddBeziers_pv(self, points):
		wg.GdipAddPathBeziers(self.ptr, *points_args(points))
	
	def AddRectangle_r(self, rect):
		wg.GdipAddPathRectangle(self.ptr, *rect_args(rect))
	
	def AddEllipse_r(self, rect):
		wg.GdipAddPathEllipse(self.ptr, *rect_args(rect))
	
	def AddArc_p3f(self, c, r, a0, a1):
		wg.GdipAddPathArc(self.ptr, *arc_args(c, r, a0, a1))

	def AddPie_p3f(self, c, r, a0, a1):
		wg.GdipAddPathPie(self.ptr, *arc_args(c, r, a0, a1))
	
	def AddLines_pv(self, points):
		wg.GdipAddPathLine2(self.ptr, *points_args(points))

	def AddPolygon_pv(self, points):
		wg.GdipAddPathPolygon(self.ptr, *points_args(points))

	def CloseFigure(self):
		wg.GdipClosePathFigure(self.ptr)
	
	def GetLastPoint(self):
		p = PointF()
		wg.GdipGetPathLastPoint(self.ptr, byref(p))
		return p.x, p.y
	
#--------------------------------------------------------------------

class Graphics(object):

	def from_hdc(cls, hdc):
		self = cls.__new__(cls)
		ptr = c_void_p()
		wg.GdipCreateFromHDC(c_ulong(hdc), byref(ptr))
		self.ptr = ptr
		return self
	
	from_hdc = classmethod(from_hdc)
	
	def from_dc(cls, dc):
		return cls.from_hdc(dc.GetSafeHdc())
	
	from_dc = classmethod(from_dc)
	
	def from_image(cls, image):
		#print "Graphics.from_image:", repr(image) ###
		#print "...", image ###
		self = cls.__new__(cls)
		ptr = c_void_p()
		wg.GdipGetImageGraphicsContext(image.ptr, byref(ptr))
		self.ptr = ptr
		return self
	
	from_image = classmethod(from_image)
	
	def __del__(self, wg = wg):
		wg.GdipDeleteGraphics(self.ptr)
	
	def __str__(self):
		return "<Graphics 0x%x>" % self.ptr.value
	
	def GetHDC(self):
		hdc = c_long()
		wg.GdipGetDC(self.ptr, byref(hdc))
		return hdc.value
	
	def ReleaseHDC(self, hdc):
		wg.GdipReleaseDC(self.ptr, hdc)
	
	def GetDpiX(self):
		result = c_float()
		wg.GdipGetDpiX(self.ptr, byref(result))
		return result.value
	
	def GetDpiY(self):
		result = c_float()
		wg.GdipGetDpiY(self.ptr, byref(result))
		return result.value
	
	def SetPageUnit(self, unit):
		self.unit = unit
		wg.GdipSetPageUnit(self.ptr, unit)
	
	def GetClipBounds(self):
		r = RectF()
		wg.GdipGetClipBounds(self.ptr, byref(r))
		return (r.x, r.y, r.x + r.width, r.y + r.height)
	
	def Save(self):
		state = c_uint()
		wg.GdipSaveGraphics(self.ptr, byref(state))
		return state.value
	
	def Restore(self, state):
		wg.GdipRestoreGraphics(self.ptr, state)
	
	def DrawImage_rr(self, image, dst_rect, src_rect):
		sl, st, sr, sb = src_rect
		dl, dt, dr, db = dst_rect
		wg.GdipDrawImageRectRect(self.ptr, image.ptr,
			c_float(dl), c_float(dt), c_float(dr - dl), c_float(db - dt),
			c_float(sl), c_float(st), c_float(sr - sl), c_float(sb - st),
			UnitPixel, None, None, None)

	def DrawPath(self, pen, path):
		wg.GdipDrawPath(self.ptr, pen.ptr, path.ptr)
	
	def FillPath(self, brush, path):
		wg.GdipFillPath(self.ptr, brush.ptr, path.ptr)
	
	def DrawAndMeasureStringWidth_2f(self, text, font, x, y, brush):
		wtext = unicode(text)
		n = len(text)
		pos = PointF(x, y)
		flags = 5 # DriverStringOptions CmapLookup+RealizedAdvance
		b = RectF()
		wg.GdipDrawDriverString(self.ptr, wtext, n, font.ptr, brush.ptr,
			byref(pos), flags, None)
		wg.GdipMeasureDriverString(self.ptr, wtext, n, font.ptr, byref(pos),
			flags, None, byref(b))
		return b.width
	
	def MeasureStringWidth(self, text, font):
		wtext = unicode(text)
		n = len(text)
		pos = PointF(0, 0)
		flags = 5 # DriverStringOptions CmapLookup+RealizedAdvance
		b = RectF()
		wg.GdipMeasureDriverString(self.ptr, wtext, n, font.ptr, byref(pos),
			flags, None, byref(b))
		return b.width

	def SetClip_PI(self, path):
		wg.GdipSetClipPath(self.ptr, path.ptr, CombineModeIntersect)

	def SetClip_rI(self, rect):
		x, y, w, h = rect_args(rect)
		wg.GdipSetClipRect(self.ptr, x, y, w, h, CombineModeIntersect)
	
	def DrawRectangle_r(self, pen, rect):
		wg.GdipDrawRectangle(self.ptr, pen.ptr, *rect_args(rect))

	def FillRectangle_r(self, brush, rect):
		#print "Graphics.FillRectangle_r:", self, brush, rect ###
		#print "... clip bounds =", self.GetClipBounds() ###
		wg.GdipFillRectangle(self.ptr, brush.ptr, *rect_args(rect))
	
	def DrawEllipse_r(self, pen, rect):
		wg.GdipDrawEllipse(self.ptr, pen.ptr, *rect_args(rect))

	def FillEllipse_r(self, brush, rect):
		wg.GdipFillEllipse(self.ptr, brush.ptr, *rect_args(rect))
	
	def DrawArc_3pf(self, pen, c, r, a0, a1):
		wg.GdipDrawArc(self.ptr, pen.ptr, *arc_args(c, r, a0, a1))
	
	def DrawPie_p3f(self, pen, c, r, a0, a1):
		wg.GdipDrawPie(self.ptr, pen.ptr, *arc_args(c, r, a0, a1))
	
	def FillPie_p3f(self, brush, c, r, a0, a1):
		wg.GdipFillPie(self.ptr, brush.ptr, *arc_args(c, r, a0, a1))
	
	def DrawPolygon_pv(self, pen, points):
		wg.GdipDrawPolygon(self.ptr, pen.ptr, *points_args(points))
	
	def FillPolygon_pv(self, brush, points):
		buf, n = points_args(points)
		wg.GdipFillPolygon(self.ptr, brush.ptr, buf, n, FillModeAlternate)
	
	def DrawBeziers_pv(self, pen,  points):
		wg.GdipDrawBeziers(self.ptr, pen.ptr, *points_args(points))
	
	def DrawLines_pv(self, pen, points):
		wg.GdipDrawLines(self.ptr, pen.ptr, *points_args(points))

	def Translate_2f(self, dx, dy):
		wg.GdipTranslateWorldTransform(self.ptr, c_float(dx), c_float(dy),
			MatrixOrderAppend)

	def Scale_2f(self, sx, sy):
		wg.GdipScaleWorldTransform(self.ptr, c_float(sx), c_float(sy),
			MatrixOrderAppend)

	def GetTransform(self):
		matrix = c_void_p()
		elems = (c_float * 6)()
		wg.GdipCreateMatrix(byref(matrix))
		wg.GdipGetWorldTransform(self.ptr, matrix)
		wg.GdipGetMatrixElements(matrix, elems)
		wg.GdipDeleteMatrix(matrix)
		return list(elems)
