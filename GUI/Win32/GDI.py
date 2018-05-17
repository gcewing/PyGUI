#--------------------------------------------------------------------
#
#   PyGUI - Win32 - GDI
#
#--------------------------------------------------------------------

LF_FACESIZE = 32

from ctypes import *
from ctypes.wintypes import *

class LOGFONT(Structure):
	_fields_ = [ ('lfHeight', c_long),
		('lfWidth', c_long),
		('lfEscapement', c_long),
		('lfOrientation', c_long),
		('lfWeight', c_long),
		('lfItalic', c_byte),
		('lfUnderline', c_byte),
		('lfStrikeOut', c_byte),
		('lfCharSet', c_byte),
		('lfOutPrecision', c_byte),
		('lfClipPrecision', c_byte),
		('lfQuality', c_byte),
		('lfPitchAndFamily', c_byte),
		('lfFaceName', c_char * LF_FACESIZE) ]

	def __init__(self):
		self.lfHeight = 10
		self.lfWidth = 0
		self.lfEscapement = 10
		self.lfOrientation = 0
		self.lfUnderline = 0
		self.lfStrikeOut = 0
		self.lfCharSet = 0 # ANSI_CHARSET
		#self.lfPitchAndFamily = 0
		self.lfOutPrecision = 0
		self.lfClipPrecision = 0
		self.lfQuality = 0
		self.lfPitchAndFamily = 2

def create_hfont(family, size, style):
	lf = LOGFONT()
	lf.lfFaceName = family
	lf.lfHeight = size
	if 'italic' in style:
		lf.lfItalic = 1
	if 'bold' in style:
		lf.lfWeight = 10
	return windll.gdi32.CreateFontIndirectA(byref(lf))
