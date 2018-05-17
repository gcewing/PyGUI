#------------------------------------------------------------------------------
#
#   PyGUI - Printing - Gtk
#
#------------------------------------------------------------------------------

import gtk, gtkunixprint
from gtk import UNIT_POINTS
from GUI import Canvas
from GUI.GPrinting import PageSetup as GPageSetup, Printable as GPrintable, \
	Paginator

gtk_paper_names = [
	gtk.PAPER_NAME_A3,
	gtk.PAPER_NAME_A4,
	gtk.PAPER_NAME_A5,
	gtk.PAPER_NAME_B5,
	gtk.PAPER_NAME_LETTER,
	gtk.PAPER_NAME_EXECUTIVE,
	gtk.PAPER_NAME_LEGAL,
]

gtk_paper_formats = {}

gtk_print_settings = gtk.PrintSettings()

def init_gtk_paper_formats():
	for gtk_name in gtk_paper_names:
		display_name = gtk.PaperSize(gtk_name).get_display_name()
		gtk_paper_formats[display_name] = gtk_name

init_gtk_paper_formats()

def gtk_default_page_setup():
	pset = gtk.PageSetup()
	pset.set_paper_size(gtk.PaperSize())
	return pset

def get_gtk_state(gtk_page_setup):
	state = {}
	state['orientation'] = gtk_page_setup.get_orientation()
	state['paper_size'] = gtk_page_setup.get_paper_size().get_name()
	state['top_margin'] = gtk_page_setup.get_top_margin(UNIT_POINTS)
	state['bottom_margin'] = gtk_page_setup.get_bottom_margin(UNIT_POINTS)
	state['left_margin'] = gtk_page_setup.get_left_margin(UNIT_POINTS)
	state['right_margin'] = gtk_page_setup.get_right_margin(UNIT_POINTS)
	return state

def set_gtk_state(gtk_page_setup, state):
	gtk_page_setup.set_orientation(state['orientation'])
	gtk_page_setup.set_paper_size(gtk.PaperSize(state['paper_size']))
	gtk_page_setup.set_top_margin(state['top_margin'], UNIT_POINTS)
	gtk_page_setup.set_bottom_margin(state['bottom_margin'], UNIT_POINTS)
	gtk_page_setup.set_left_margin(state['left_margin'], UNIT_POINTS)
	gtk_page_setup.set_right_margin(state['right_margin'], UNIT_POINTS)

#------------------------------------------------------------------------------

class PageSetup(GPageSetup):

	_printer_name = ""
	_left_margin = 36
	_top_margin = 36
	_right_margin = 36
	_bottom_margin = 36
	
	def __init__(self):
		self._gtk_page_setup = gtk_default_page_setup()

	def __getstate__(self):
		state = GPageSetup.__getstate__(self)
		state['_gtk_page_setup'] = get_gtk_state(self._gtk_page_setup)
		return state
	
	def __setstate__(self, state):
		gtk_setup = gtk_default_page_setup()
		self._gtk_page_setup = gtk_setup
		gtk_state = state.pop('_gtk_page_setup', None)
		if gtk_state:
			set_gtk_state(gtk_setup, gtk_state)
			self.margins = state['margins']
			self.printer_name = state['printer_name']
		else:
			GPageSetup.__setstate__(state)

	def get_paper_name(self):
		return self._gtk_page_setup.get_paper_size().get_display_name()
	
	def set_paper_name(self, x):
		psize = gtk.PaperSize(gtk_paper_formats.get(x) or x)
		self._gtk_page_setup.set_paper_size(psize)
	
	def get_paper_width(self):
		return self._gtk_page_setup.get_paper_width(UNIT_POINTS)
	
	def set_paper_width(self, x):
		self._gtk_page_setup.set_paper_width(x, UNIT_POINTS)

	def get_paper_height(self):
		return self._gtk_page_setup.get_paper_height(UNIT_POINTS)

	def set_paper_height(self, x):
		self._gtk_page_setup.set_paper_height(x, UNIT_POINTS)
	
	def get_orientation(self):
		o = self._gtk_page_setup.get_orientation()
		if o in (gtk.PAGE_ORIENTATION_LANDSCAPE,
			gtk.PAGE_ORIENTATION_REVERSE_LANDSCAPE):
				return 'landscape'
		else:
			return 'portrait'
	
	def set_orientation(self, x):
		if x == 'landscape':
			o = gtk.PAGE_ORIENTATION_LANDSCAPE
		else:
			o = gtk.PAGE_ORIENTATION_PORTRAIT
		self._gtk_page_setup.set_orientation(o)
	
	def get_left_margin(self):
		return self._left_margin

	def get_top_margin(self):
		return self._top_margin

	def get_right_margin(self):
		return self._right_margin

	def get_bottom_margin(self):
		return self._bottom_margin
	
	def set_left_margin(self, x):
		self._left_margin = x

	def set_top_margin(self, x):
		self._top_margin = x

	def set_right_margin(self, x):
		self._right_margin = x

	def set_bottom_margin(self, x):
		self._bottom_margin = x
	
	def get_printer_name(self):
		return self._printer_name
	
	def set_printer_name(self, x):
		self._printer_name = x

#------------------------------------------------------------------------------

class Printable(GPrintable):

	def print_view(self, page_setup, prompt = True):
		global gtk_print_settings
		paginator = Paginator(self, page_setup)
		
		def draw_page(_, gtk_print_context, page_num):
			cairo_context = gtk_print_context.get_cairo_context()
			canvas = Canvas._from_cairo_context(cairo_context)
			paginator.draw_page(canvas, page_num)
		
		gtk_op = gtk.PrintOperation()
		gtk_op.set_print_settings(gtk_print_settings)
		gtk_op.set_default_page_setup(page_setup._gtk_page_setup)
		gtk_op.set_n_pages(paginator.num_pages)
		gtk_op.set_use_full_page(True)
		gtk_op.set_unit(UNIT_POINTS)
		gtk_op.connect('draw-page', draw_page)
		if prompt:
			action = gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG
		else:
			action = gtk.PRINT_OPERATION_ACTION_PRINT
		result = gtk_op.run(action)
		if result == gtk.PRINT_OPERATION_RESULT_APPLY:
			gtk_print_settings = gtk_op.get_print_settings()

#------------------------------------------------------------------------------

def present_page_setup_dialog(page_setup):
	old_setup = page_setup._gtk_page_setup
	ps = gtk.PrintSettings()
	new_setup = gtk.print_run_page_setup_dialog(None, old_setup, ps)
	if get_gtk_state(old_setup) <> get_gtk_state(new_setup):
		page_setup._gtk_page_setup = new_setup
		return True
	else:
		return False
