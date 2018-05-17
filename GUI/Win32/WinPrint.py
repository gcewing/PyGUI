#------------------------------------------------------------------------------
#
#   PyGUI - Win32 API - Printing
#
#------------------------------------------------------------------------------

from ctypes import *
from ctypes.wintypes import *

comdlg32 = windll.comdlg32
gdi32 = windll.gdi32

PD_ALLPAGES = 0x0
PD_RETURNDC = 0x100

LOGPIXELSX = 88
LOGPIXELSY = 90
PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113

LPDWORD = POINTER(DWORD)
LPHANDLE = POINTER(HANDLE)
LPPOINT = POINTER(POINT)
LPPRINTHOOKPROC = c_void_p
LPSETUPHOOKPROC = c_void_p
ABORTPROC = CFUNCTYPE(c_int, HDC, c_int)
LPPRINTER_DEFAULTS = c_void_p

class PRINTDLG(Structure):

	_pack_ = 2
	_fields_ = [
		('lStructSize', DWORD),
		('hwndOwner', HWND),
		('hDevMode', HGLOBAL),
		('hDevNames', HGLOBAL),
		('hDC', HDC),
		('Flags', DWORD),
		('nFromPage', WORD),
		('nToPage', WORD),
		('nMinPage', WORD),
		('nMaxPage', WORD),
		('nCopies', WORD),
		('hInstance', HINSTANCE),
		('lCustData', LPARAM),
		('lpfnPrintHook', LPPRINTHOOKPROC),
		('lpfnSetupHook', LPSETUPHOOKPROC),
		('lpPrintTemplateName', LPCSTR),
		('lpSetupTemplateName', LPCSTR),
		('hPrintTemplate', HGLOBAL),
		('hSetupTemplate', HGLOBAL),
	]
	
	def __init__(self):
		self.lStructSize = sizeof(PRINTDLG)

class DOCINFO(Structure):

	_fields_ = [
		('cbSize', c_int),
		('lpszDocName', LPCSTR),
		('lpszOutput', LPCSTR),
		('lpszDatatype', LPCSTR),
		('fwType', DWORD),
	]
	
	def __init__(self):
		self.cbSize = sizeof(DOCINFO)

class FORM_INFO_1_W(Structure):

	_fields_ = [
		('Flags', DWORD),
		('pName', LPWSTR),
		('Size', SIZEL),
		('ImageableArea', RECTL),
	]

_PrintDlg = comdlg32.PrintDlgA
_PrintDlg.argtypes = [POINTER(PRINTDLG)]

SetAbortProc = gdi32.SetAbortProc
SetAbortProc.argtypes = [HDC, ABORTPROC]

StartDoc = gdi32.StartDocA
StartDoc.argtypes = [HDC, POINTER(DOCINFO)]

StartPage = gdi32.StartPage
StartPage.argtypes = [HDC]

EndPage = gdi32.EndPage
EndPage.argtypes = [HDC]

EndDoc = gdi32.EndDoc
EndDoc.argtypes = [HDC]

DeleteDC = gdi32.DeleteDC
DeleteDC.argtypes = [HDC]

CommDlgExtendedError = comdlg32.CommDlgExtendedError
CommDlgExtendedError.argtypes = []

def PrintDlg(pd):
	pd.nFromPage = pd.nMinPage
	pd.nToPage = pd.nMaxPage
	pd.Flags = PD_RETURNDC
	#if pd.nMaxPage > pd.nMinPage:
	#	pd.Flags |= PD_PAGENUMS
	result = _PrintDlg(pd)
	if result == 0:
		err = CommDlgExtendedError()
		if err <> 0:
			raise EnvironmentError("Common Dialog error %s" % err)
	return bool(result)

def GetPrintingOffset(hdc):
	dpix = gdi32.GetDeviceCaps(hdc, LOGPIXELSX)
	dpiy = gdi32.GetDeviceCaps(hdc, LOGPIXELSY)
	offx = gdi32.GetDeviceCaps(hdc, PHYSICALOFFSETX)
	offy = gdi32.GetDeviceCaps(hdc, PHYSICALOFFSETY)
	return 72.0 * offx / dpix, 72.0 * offy / dpiy

def abort_proc(hdc, err):
	return printing_aborted

def install_abort_proc(hdc):
	global printing_aborted
	printing_aborted = False
	SetAbortProc(hdc, ABORTPROC(abort_proc))
