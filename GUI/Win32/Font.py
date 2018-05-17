#--------------------------------------------------------------------
#
#   PyGUI - Font - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32gui as gui, win32ui as ui, win32api as api
from GUI import export
from WinUtils import win_none
import GUI.GDI as gdi
import GUI.GDIPlus as gdip
from GUI.GFonts import Font as GFont

#win_family_map = {
#	"Decorative": wc.FF_DECORATIVE | wc.DEFAULT_PITCH,
#	"Fixed":      wc.FF_MODERN | wc.FIXED_PITCH,
#	"Courier":    wc.FF_MODERN | wc.FIXED_PITCH,
#	"Modern":     wc.FF_MODERN | wc.DEFAULT_PITCH,
#	"Serif":      wc.FF_ROMAN | wc.VARIABLE_PITCH,
#	"Roman":      wc.FF_ROMAN | wc.VARIABLE_PITCH,
#	"Times":      wc.FF_ROMAN | wc.VARIABLE_PITCH,
#	"Sans":       wc.FF_SWISS | wc.VARIABLE_PITCH,
#	"Helvetica":  wc.FF_SWISS | wc.VARIABLE_PITCH,
#	"Script":     wc.FF_SCRIPT | wc.DEFAULT_PITCH,
#	"Cursive":    wc.FF_SCRIPT | wc.DEFAULT_PITCH,
#}

#win_default_pf = wc.FF_DONTCARE | wc.DEFAULT_PITCH

def win_create_font(**kwds):
	#  Work around bug in CreateFont
	for name in 'italic', 'underline':
		if name in kwds and not kwds[name]:
			del kwds[name]
	return ui.CreateFont(kwds)

#def win_pf_to_name(pf):
#	if pf & 0x3 == wc.FIXED_PITCH:
#		return "Fixed"
#	for name, npf in win_family_map.iteritems():
#		if pf & 0xf0 == npf & 0xf0:
#			return name
#	return "Unknown"

win_generic_family_map = {
	"Sans": "Arial",
	"Serif": "Times New Roman",
	"Fixed": "Courier New",
	"Times": "Times New Roman",
	"Courier": "Courier New",
}

#  PyWin32 build 212 and earlier negate the value of the height
#  passed to CreateFont.

pywin32_info = api.GetFileVersionInfo(api.__file__, '\\')
pywin32_build = pywin32_info['FileVersionLS'] >> 16
if pywin32_build <= 212:
	win_height_sign = 1
else:
	win_height_sign = -1

#--------------------------------------------------------------------

class Font(GFont):
	#  _win_font    PyCFont
	#  _win_gfont   GDIPlus.Font

	def __init__(self, family = "Times", size = 12, style = []):
		win_family = win_generic_family_map.get(family, family)
		self._family = family
		self._win_family = win_family
		self._size = size
		self._style = style
		if 'bold' in style:
			win_weight = wc.FW_BOLD
		else:
			win_weight = wc.FW_NORMAL
		#print "Font: calling win_create_font" ###
		height = int(round(size))
		#print "Font: height =", height ###
		win_font = win_create_font(
			name = win_family,
			height = win_height_sign * height,
			weight = win_weight,
			italic = 'italic' in style)
			#pitch_and_family = 0) ###win_family_map.get(family, win_default_pf))
		self._win_font = win_font
		self._win_update_metrics()
		#global dc ###
		#dc = win_none.GetDC()
		#dc.SelectObject(win_font)
		#self._win_gfont = gdip.Font.from_hdc(dc.GetSafeHdc())
		#win_none.ReleaseDC(dc)
	
#	def __init__(self, family = "Times", size = 12, style = []):
#		self._family = family
#		self._size = size
#		self._style = style
#		hfont = gdi.create_hfont(family, size, style)
#		self._win_hfont = hfont
#		self._win_update_metrics()

	def get_family(self):
		return self._family

	def get_size(self):
		return self._size

	def get_style(self):
		return self._style
	
	def get_ascent(self):
		return self._ascent
	
	def get_descent(self):
		return self._descent
	
	def get_leading(self):
		return self._leading
	
	def get_cap_height(self):
		return self._ascent - self._internal_leading
	
	def get_x_height(self):
		return self._ascent - self._internal_leading - self._descent
	
	def get_height(self):
		return self._ascent + self._descent
	
	def get_line_height(self):
		return self._ascent + self._descent + self._leading
	
	def _win_update_metrics(self):
		dc = win_none.GetDC()
		dc.SelectObject(self._win_font)
		met = dc.GetTextMetrics()
		self._ascent = met['tmAscent']
		self._descent = met['tmDescent']
		self._internal_leading = met['tmInternalLeading']
		self._leading = met['tmExternalLeading']
		self._win_overhang = met['tmOverhang']
		#print "Font: tmOverhang =", self._win_overhang ###
		win_none.ReleaseDC(dc)
		self._win_gdip_font = gdip.Font(self._win_family, self._size, self._style)
	
	def _width(self, s):
		dc = win_none.GetDC()
		dc.SelectObject(self._win_font)
		w, h = dc.GetTextExtent(s)
		win_none.ReleaseDC(dc)
		return w
	
#	def _width(self, s):
#		dc = win_none.GetDC()
#		g = gdip.Graphics.from_hdc(dc.GetSafeHdc())
#		w = g.MeasureStringWidth(s, self._win_gdip_font)
#		win_none.ReleaseDC(dc)
#		return w

	def info(self):
		return "<Font family=%r size=%s style=%s ascent=%s descent=%s " \
			"leading=%s height=%s cap_height=%s x_height=%s line_height=%s>" % \
			(self.family, self.size, self.style, self.ascent, self.descent, 
			self.leading, self.height, self.cap_height, self.x_height,
			self.line_height)
	
	def tm_info(self):
		win = ui.CreateWnd()
		dc = win.GetDC()
		dc.SelectObject(self._win_font)
		tm = dc.GetTextMetrics()
		win.ReleaseDC(dc)
		return tm

#	def _from_win_logfont(cls, lf):
#		#print "Font._from_win_logfont:", lf ###
#		#for name in dir(lf): ###
#		#	print name, "=", getattr(lf, name) ###
#		font = cls.__new__(cls)
#		font._family = win_pf_to_name(lf.lfPitchAndFamily)
#		font._size = abs(lf.lfHeight)
#		style = []
#		if lf.lfWeight >= wc.FW_BOLD:
#			style.append('bold')
#		if lf.lfItalic:
#			style.append('italic')
#		font._style = style
#		font._win_font = win_create_font(
#			width = lf.lfWidth,
#			#height = abs(lf.lfHeight),
#			height = lf.lfHeight,
#			weight = lf.lfWeight,
#			italic = lf.lfItalic,
#			underline = lf.lfUnderline,
#			pitch_and_family = lf.lfPitchAndFamily,
#			charset = lf.lfCharSet)
#		font._win_update_metrics()
#		return font
#
#	_from_win_logfont =  classmethod(_from_win_logfont)

	def _from_win(cls, win):
		dc = win.GetDC()
		family = dc.GetTextFace()
		tm = dc.GetTextMetrics()
		#print family, tm
		size = tm['tmAscent'] - tm['tmInternalLeading'] + tm['tmDescent']
		style = []
		if tm['tmWeight'] >=  wc.FW_BOLD:
			style.append('bold')
		if tm['tmItalic']:
			style.append('italic')
		win.ReleaseDC(dc)
		return Font(family, size, style)

	_from_win = classmethod(_from_win)

export(Font)
