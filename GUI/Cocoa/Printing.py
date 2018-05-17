#------------------------------------------------------------------------------
#
#   PyGUI - Printing - Cocoa
#
#------------------------------------------------------------------------------

from AppKit import NSPrintInfo, NSPageLayout, NSPrintOperation, \
	NSKeyedArchiver, NSKeyedUnarchiver, NSData, NSAutoPagination, \
	NSPortraitOrientation, NSLandscapeOrientation, NSOKButton
from GUI.GPrinting import PageSetup as GPageSetup, Printable as GPrintable

ns_to_generic_orientation = {
	NSPortraitOrientation: 'portrait',
	NSLandscapeOrientation: 'landscape',
}

generic_to_ns_orientation = {
	'portrait': NSPortraitOrientation,
	'landscape': NSLandscapeOrientation,
}

#------------------------------------------------------------------------------

class PageSetup(GPageSetup):

	def __init__(self):
		ns_pi = NSPrintInfo.sharedPrintInfo().copy()
		ns_pi.setLeftMargin_(36)
		ns_pi.setTopMargin_(36)
		ns_pi.setRightMargin_(36)
		ns_pi.setBottomMargin_(36)
		ns_pi.setHorizontalPagination_(NSAutoPagination)
		self._ns_print_info = ns_pi
	
	def __getstate__(self):
		state = GPageSetup.__getstate__(self)
		data = NSKeyedArchiver.archivedDataWithRootObject_(self._ns_print_info)
		state['_ns_print_info'] = data.bytes()
		return state
	
	def __setstate__(self, state):
		bytes = state.pop('_ns_print_info', None)
		if bytes:
			data = NSData.dataWithBytes_length_(bytes, len(bytes))
			self._ns_print_info = NSKeyedArchiver.unarchiveObjectWithData_(data)
		else:
			GPageSetup.__setstate__(self, state)
	
	def copy(self, other):
		result = PageSetup.__new__()
		result._ns_print_info = other._ns_print_info.copy()

	def get_paper_name(self):	
		return self._ns_print_info.paperName()

	def set_paper_name(self, x):	
		self._ns_print_info.setPaperName_(x)
	
	def get_paper_size(self):
		return tuple(self._ns_print_info.paperSize())

	def set_paper_size(self, x):
		self._ns_print_info.setPaperSize_(x)

	def get_paper_width(self):
		return self.paper_size[0]

	def set_paper_width(self, x):
		self.paper_size = x, self.paper_height

	def get_paper_height(self):
		return self.paper_size[1]

	def set_paper_height(self, x):
		self.paper_size = self.paper_width, x

	def get_left_margin(self):
		return self._ns_print_info.leftMargin()

	def set_get_left_margin(self, x):
		self._ns_print_info.setLefMargin_(x)

	def get_right_margin(self):
		return self._ns_print_info.rightMargin()

	def set_get_right_margin(self, x):
		self._ns_print_info.setRightMargin_(x)

	def get_top_margin(self):
		return self._ns_print_info.topMargin()

	def set_get_top_margin(self, x):
		self._ns_print_info.setTopMargin_(x)

	def get_bottom_margin(self):
		return self._ns_print_info.bottomMargin()

	def set_get_bottom_margin(self, x):
		self._ns_print_info.setBottomMargin_(x)
	
	def get_orientation(self):
		return ns_to_generic_orientation[self._ns_print_info.orientation()]
	
	def set_orientation(self, x):
		nso = generic_to_ns_orientation.get(x, 'portrait')
		self._ns_print_info.setOrientation_(nso)
	
	def get_printable_rect(self):
		l, b, w, h = self._ns_print_info.imageablePageBounds()
		return (l, b - h, l + w, b)
	
	def get_printer_name(self):
		return self._ns_print_info.printer().name()
	
	def set_printer_name(self, x):
		self._ns_print_info.setPrinter_(NSPrinter.printerWithName_(x))

#------------------------------------------------------------------------------

class Printable(GPrintable):

	def print_view(self, page_setup, prompt = True):
		ns_op = NSPrintOperation.printOperationWithView_printInfo_(
			self._ns_inner_view, page_setup._ns_print_info)
		ns_op.setShowsPrintPanel_(prompt)
		ns_op.runOperation()

#------------------------------------------------------------------------------

def present_page_setup_dialog(page_setup):
	result = NSPageLayout.pageLayout().runModalWithPrintInfo_(page_setup._ns_print_info)
	return result == NSOKButton
