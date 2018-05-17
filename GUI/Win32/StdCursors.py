#--------------------------------------------------------------------------
#
#		Python GUI - Standard Cursors - Win32
#
#--------------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI import Cursor

__all__ = [
	'arrow',
	'ibeam', 
	'crosshair', 
	'fist', 
	'hand', 
	'finger', 
	'invisible', 
]

def win_get_std_cursor(id):
	app = ui.GetApp()
	win_app = getattr(app, '_win_app', app)
	hcursor = win_app.LoadStandardCursor(id)
	return Cursor._from_win_cursor(hcursor)

arrow = win_get_std_cursor(wc.IDC_ARROW)
ibeam = win_get_std_cursor(wc.IDC_IBEAM)
crosshair = win_get_std_cursor(wc.IDC_CROSS)
fist = Cursor("cursors/fist.tiff")
hand = Cursor("cursors/hand.tiff")
finger = win_get_std_cursor(wc.IDC_HAND)
invisible = Cursor._from_win_cursor(0)

def empty_cursor():
	return invisible

# Win32 only
wait = win_get_std_cursor(wc.IDC_WAIT)
up_arrow = win_get_std_cursor(wc.IDC_UPARROW)
size_all = win_get_std_cursor(wc.IDC_SIZEALL)
size_w_e = win_get_std_cursor(wc.IDC_SIZEWE)
size_n_s = win_get_std_cursor(wc.IDC_SIZENS)
size_nw_se = win_get_std_cursor(wc.IDC_SIZENWSE)
size_ne_sw = win_get_std_cursor(wc.IDC_SIZENESW)

