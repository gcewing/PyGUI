#------------------------------------------------------------------------------
#
#   PyGUI - Win32 API - Page setup dialog
#
#------------------------------------------------------------------------------

from ctypes import *
from ctypes.wintypes import *

comdlg32 = windll.comdlg32
kernel32 = windll.kernel32

CCHDEVICENAME = 32
CCHFORMNAME = 32

PSD_MARGINS = 0x2
PSD_INTHOUSANDTHSOFINCHES = 0x4
PSD_RETURNDEFAULT = 0x400

LPPAGESETUPHOOK = c_void_p
LPPAGEPAINTHOOK = c_void_p

class PAGESETUPDLG(Structure):
	_fields_ = [
		('lStructSize', DWORD),
		('hwndOwner', HWND),
		('hDevMode', HGLOBAL),
		('hDevNames', HGLOBAL),
		('Flags', DWORD),
		('ptPaperSize', POINT),
		('rtMinMargin', RECT),
		('rtMargin', RECT),
		('hInstance', HINSTANCE),
		('lCustData', LPARAM),
		('lpfnPageSetupHook', LPPAGESETUPHOOK),
		('lpfnPagePaintHook', LPPAGEPAINTHOOK),
		('lpPageSetupTemplateName', LPCSTR),
		('hPageSetupTemplate', HGLOBAL),
	]
	
	def __del__(self):
		print "PAGESETUPDLG.__del__" ###
		GlobalFree(self.hDevMode)
		GlobalFree(self.hDevNames)

class DEVMODE(Structure):
	_fields_ = [
		('dmDeviceName', c_char * CCHDEVICENAME),
		('dmSpecVersion', WORD),
		('dmDriverVersion', WORD),
		('dmSize', WORD),
		('dmDriverExtra', WORD),
		('dmFields', DWORD),
		('dmOrientation', c_short),
		('dmPaperSize', c_short),
		('dmPaperLength', c_short),
		('dmPaperWidth', c_short),
		('dmScale', c_short),
		('dmCopies', c_short),
		('dmDefaultSource', c_short),
		('dmPrintQuality', c_short),
		('dmColor', c_short),
		('dmDuplex', c_short),
		('dmYResolution', c_short),
		('dmTTOption', c_short),
		('dmCollate', c_short),
		('dmFormName', c_char * CCHFORMNAME),
		('dmLogPixels', WORD),
		('dmBitsPerPel', DWORD),
		('dmPelsWidth', DWORD),
		('dmPelsHeight', DWORD),
		('dmDisplayFlags', DWORD),
		('dmDisplayFrequency', DWORD),
		('dmICMMethod', DWORD),
		('dmICMIntent', DWORD),
		('dmMediaType', DWORD),
		('dmDitherType', DWORD),
		('dmReserved1', DWORD),
		('dmReserved2', DWORD),
		('dmPanningWidth', DWORD),
		('dmPanningHeight', DWORD),
	]

class DEVNAMES(Structure):
	_fields_ = [
		('wDriverOffset', WORD),
		('wDeviceOffset', WORD),
		('wOutputOffset', WORD),
		('wDefault', WORD),
	]

_PageSetupDlg = comdlg32.PageSetupDlgA
_PageSetupDlg.argtypes = [POINTER(PAGESETUPDLG)]

GlobalAlloc = kernel32.GlobalAlloc
GlobalAlloc.argtypes = [UINT, DWORD]

GlobalSize = kernel32.GlobalSize
GlobalSize.argtypes = [HGLOBAL]

GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = [HGLOBAL]

GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = [HGLOBAL]

GlobalFree = kernel32.GlobalFree
GlobalFree.argtypes = [HGLOBAL]

def PageSetupDlg(psd):
	psd.Flags = PSD_INTHOUSANDTHSOFINCHES | PSD_MARGINS
	return bool(_PageSetupDlg(psd))

def get_handle_contents(h):
	n = GlobalSize(h)
	p = GlobalLock(h)
	data = string_at(p, n)
	GlobalUnlock(h)
	return data

def handle_with_contents(data):
	n = len(data)
	h = GlobalAlloc(n)
	p = GlobalLock(h)
	memmove(p, data, n)
	GlobalUnlock(h)
	return h

def lock_devmode_handle(h):
	p = c_void_p(GlobalLock(h))
	dmp = cast(p, POINTER(DEVMODE))
	return dmp[0]

class DevNames(object):

	def __init__(self, hdevnames):
		a = GlobalLock(hdevnames)
		p = c_void_p(a)
		dnp = cast(p, POINTER(DEVNAMES))
		dn = dnp[0]
		self.driver = c_char_p(a + dn.wDriverOffset).value
		self.device = c_char_p(a + dn.wDeviceOffset).value
		self.output = c_char_p(a + dn.wOutputOffset).value
		self.default = dn.wDefault
		GlobalUnlock(hdevnames)

def get_defaults():
	psd = PAGESETUPDLG()
	psd.lStructSize = sizeof(PAGESETUPDLG)
	psd.Flags = PSD_INTHOUSANDTHSOFINCHES | PSD_RETURNDEFAULT
	_PageSetupDlg(psd)
	return psd

if __name__ == "__main__":
	def dump_psd(header, psd):
		print "%s:" % header, psd
		for name, _ in PAGESETUPDLG._fields_:
			print "  %s = %r" % (name, getattr(psd, name))
	psd = PAGESETUPDLG()
	psd.lStructSize = sizeof(PAGESETUPDLG)
	dump_psd("Initial psd", psd)
	result = _PageSetupDlg(psd)
	print "Result:", result
	dump_psd("Final psd", psd)
	#print "DevMode:", repr(get_handle_contents(psd.hDevMode)[:sizeof(DEVMODE)])
	dm = lock_devmode_handle(psd.hDevMode)
	print "dmDeviceName:", dm.dmDeviceName
	#print "DevNames:", repr(get_handle_contents(psd.hDevNames))
