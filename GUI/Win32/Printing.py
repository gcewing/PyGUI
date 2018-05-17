#------------------------------------------------------------------------------
#
#   PyGUI - Printing - Win32
#
#------------------------------------------------------------------------------

import WinPageSetup as wps, WinPrint as wp
import win32print as wp2
from GUI.GPrinting import PageSetup as GPageSetup, Printable as GPrintable, \
	Paginator
from GUI import Canvas

#------------------------------------------------------------------------------

win_paper_names = {
	1: "Letter", # Letter 8 1/2 x 11 in
	2: "Letter Small", # Letter Small 8 1/2 x 11 in
	3: "Tabloid", # Tabloid 11 x 17 in
	4: "Ledger", # Ledger 17 x 11 in
	5: "Legal", # Legal 8 1/2 x 14 in
	6: "Statement", # Statement 5 1/2 x 8 1/2 in
	7: "Executive", # Executive 7 1/4 x 10 1/2 in
	8: "A3", # A3 297 x 420 mm
	9: "A4", # A4 210 x 297 mm
	10: "A4 Small", # A4 Small 210 x 297 mm
	11: "A5", # A5 148 x 210 mm
	12: "B4 (JIS)", # B4 (JIS) 250 x 354
	13: "B5 (JIS)", # B5 (JIS) 182 x 257 mm
	14: "Folio", # Folio 8 1/2 x 13 in
	15: "Quarto", # Quarto 215 x 275 mm
	16: "10x14", # 10x14 in
	17: "11x17", # 11x17 in
	18: "Note", # Note 8 1/2 x 11 in
	19: "Envelope #9", # Envelope #9 3 7/8 x 8 7/8
	20: "Envelope #10", # Envelope #10 4 1/8 x 9 1/2
	21: "Envelope #11", # Envelope #11 4 1/2 x 10 3/8
	22: "Envelope #12", # Envelope #12 4 \276 x 11
	23: "Envelope #14", # Envelope #14 5 x 11 1/2
	24: "C Sheet", # C size sheet
	25: "D Sheet", # D size sheet
	26: "E Sheet", # E size sheet
	27: "Envelope DL", # Envelope DL 110 x 220mm
	28: "Envelope C5", # Envelope C5 162 x 229 mm
	29: "Envelope C3", # Envelope C3  324 x 458 mm
	30: "Envelope C4", # Envelope C4  229 x 324 mm
	31: "Envelope C6", # Envelope C6  114 x 162 mm
	32: "Envelope C65", # Envelope C65 114 x 229 mm
	33: "Envelope B4", # Envelope B4  250 x 353 mm
	34: "Envelope B5", # Envelope B5  176 x 250 mm
	35: "Envelope B6", # Envelope B6  176 x 125 mm
	36: "Envelope", # Envelope 110 x 230 mm
	37: "Envelope Monarch", # Envelope Monarch 3.875 x 7.5 in
	38: "6 3/4 Envelope", # 6 3/4 Envelope 3 5/8 x 6 1/2 in
	39: "US Std Fanfold", # US Std Fanfold 14 7/8 x 11 in
	40: "German Std Fanfold", # German Std Fanfold 8 1/2 x 12 in
	41: "German Legal Fanfold", # German Legal Fanfold 8 1/2 x 13 in
	42: "B4", # B4 (ISO) 250 x 353 mm
	43: "Japanese Postcard", # Japanese Postcard 100 x 148 mm
	44: "9x11", # 9 x 11 in
	45: "10x11", # 10 x 11 in
	46: "15x11", # 15 x 11 in
	47: "Envelope Invite", # Envelope Invite 220 x 220 mm
	#48: "", # RESERVED--DO NOT USE
	#49: "", # RESERVED--DO NOT USE
	50: "Letter Extra", # Letter Extra 9 \275 x 12 in
	51: "Legal Extra", # Legal Extra 9 \275 x 15 in
	52: "Tabloid Extra", # Tabloid Extra 11.69 x 18 in
	53: "A4 Extra", # A4 Extra 9.27 x 12.69 in
	54: "Letter Transverse", # Letter Transverse 8 \275 x 11 in
	55: "A4 Transverse", # A4 Transverse 210 x 297 mm
	56: "Letter Extra Transverse", # Letter Extra Transverse 9\275 x 12 in
	57: "SuperA", # SuperA/SuperA/A4 227 x 356 mm
	58: "SuperB", # SuperB/SuperB/A3 305 x 487 mm
	59: "Letter Plus", # Letter Plus 8.5 x 12.69 in
	60: "A4 Plus", # A4 Plus 210 x 330 mm
	61: "A5 Transverse", # A5 Transverse 148 x 210 mm
	62: "B5 (JIS) Transverse", # B5 (JIS) Transverse 182 x 257 mm
	63: "A3 Extra", # A3 Extra 322 x 445 mm
	64: "A5 Extra", # A5 Extra 174 x 235 mm
	65: "B5 (ISO) Extra", # B5 (ISO) Extra 201 x 276 mm
	66: "A2", # A2 420 x 594 mm
	67: "A3 Transverse", # A3 Transverse 297 x 420 mm
	68: "A3 Extra Transverse", # A3 Extra Transverse 322 x 445 mm
}

win_paper_codes = dict([(name, code)
	for (code, name) in win_paper_names.iteritems()])
	
def ti_to_pts(x):
	return x * 0.072

def pts_to_ti(x):
	return int(round(x / 0.072))

#------------------------------------------------------------------------------

class PageSetup(GPageSetup):

	def __new__(cls):
		self = GPageSetup.__new__(cls)
		self._win_psd = wps.get_defaults()
		return self
	
	def __init__(self):
		self.margins = (36, 36, 36, 36)
	
	def __getstate__(self):
		psd = self._win_psd
		state = GPageSetup.__getstate__(self)
		state['_win_devmode'] = wps.get_handle_contents(psd.hDevMode)
		state['_win_devnames'] = wps.get_handle_contents(psd.hDevNames)
		return state
	
	def __setstate__(self, state):
		psd = self._win_psd
		dm = state.pop('_win_devmode', None)
		dn = state.pop('_win_devnames', None)
		GPageSetup.__setstate__(self, state)
		if dm:
			wps.GlobalFree(psd.hDevMode)
			psd.hDevMode = handle_with_contents(dm)
		if dn:
			wps.GlobalFree(psd.hDevNames)
			psd.hDevNames = handle_with_contents(dn)
	
	def _win_lock_devmode(self):
		return wps.lock_devmode_handle(self._win_psd.hDevMode)
	
	def _win_unlock_devmode(self):
		wps.GlobalUnlock(self._win_psd.hDevMode)
	
	def get_printable_rect(self):
		psd = self._win_psd
		pw, ph = self.paper_size
		mm = psd.rtMinMargin
		ml = ti_to_pts(mm.left)
		mt = ti_to_pts(mm.top)
		mr = ti_to_pts(mm.right)
		mb = ti_to_pts(mm.bottom)
		return (ml, mt, pw - mr, ph - mb)
	
	def get_paper_name(self):
		dm = self._win_lock_devmode()
		result = win_paper_names.get(dm.dmPaperSize, "Custom")
		self._win_unlock_devmode()
		return result
	
	def set_paper_name(self, name):
		dm = self._win_lock_devmode()
		dm.dmPaperSize = win_paper_codes.get(name, 0)
		self._win_unlock_devmode()
	
	def get_paper_width(self):
		return ti_to_pts(self._win_psd.ptPaperSize.x)

	def get_paper_height(self):
		return ti_to_pts(self._win_psd.ptPaperSize.y)
	
	def set_paper_width(self, v):
		self._win_psd.ptPaperSize.x = pts_to_ti(v)

	def set_paper_height(self, v):
		self._win_psd.ptPaperSize.y = pts_to_ti(v)
	
	def get_left_margin(self):
		return ti_to_pts(self._win_psd.rtMargin.left)

	def get_top_margin(self):
		return ti_to_pts(self._win_psd.rtMargin.top)

	def get_right_margin(self):
		return ti_to_pts(self._win_psd.rtMargin.right)

	def get_bottom_margin(self):
		return ti_to_pts(self._win_psd.rtMargin.bottom)
	
	def set_left_margin(self, v):
		self._win_psd.rtMargin.left = pts_to_ti(v)

	def set_top_margin(self, v):
		self._win_psd.rtMargin.top = pts_to_ti(v)

	def set_right_margin(self, v):
		self._win_psd.rtMargin.right = pts_to_ti(v)

	def set_bottom_margin(self, v):
		self._win_psd.rtMargin.bottom = pts_to_ti(v)
	
	def get_orientation(self):
		dm = self._win_lock_devmode()
		result = win_orientation_names.get(dm.dmOrientation, 'portrait')
		self._win_unlock_devmode()
		return result
	
	def set_orientation(self, v):
		dm = self._win_lock_devmode()
		dm.dmOrientation = win_orientation_codes.get(v, 1)
		self._win_unlock_devmode()
	
	def get_printer_name(self):
		dm = self._win_lock_devmode()
		result = dm.dmDeviceName
		self._win_unlock_devmode()
		return result
	
	def set_printer_name(self, v):
		dm = self._win_lock_devmode()
		dm.dmDeviceName = v
		self._win_unlock_devmode()

#------------------------------------------------------------------------------

class Printable(GPrintable):

	def print_view(self, page_setup, prompt = True):
		paginator = Paginator(self, page_setup)
		psd = page_setup._win_psd
		pd = wp.PRINTDLG()
		pd.hDevMode = psd.hDevMode
		pd.hDevNames = psd.hDevNames
		pd.nMinPage = 1
		pd.nMaxPage = paginator.num_pages
		pd.nCopies = 1
		if wp.PrintDlg(pd):
			title = self.print_title
			di = wp.DOCINFO()
			di.lpszDocName = title
			devnames = wps.DevNames(psd.hDevNames)
			if devnames.output == "FILE:":
				from FileDialogs import request_new_file
				f = request_new_file("Print '%s' to file:" % title)
				if not f:
					return
				output_path = f.path
				di.lpszOutput = output_path
			try:
				hdc = pd.hDC
				dx, dy = wp.GetPrintingOffset(hdc)
				print "TODO: Printable: Implement a Cancel dialog" ###
				#wp.install_abort_proc(hdc)
				wp.StartDoc(hdc, di)
				for page_num in xrange(pd.nFromPage - 1, pd.nToPage):
					wp.StartPage(hdc)
					canvas = Canvas._from_win_hdc(hdc, for_printing = True)
					canvas.translate(-dx, -dy)
					paginator.draw_page(canvas, page_num)
					wp.EndPage(hdc)
				wp.EndDoc(hdc)
			finally:
				wp.DeleteDC(hdc)

#------------------------------------------------------------------------------

def present_page_setup_dialog(page_setup):
	return wps.PageSetupDlg(page_setup._win_psd)
