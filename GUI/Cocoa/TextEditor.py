#------------------------------------------------------------------------------
#
#   Python GUI - Text Editor - Cocoa
#
#------------------------------------------------------------------------------

from AppKit import NSTextView, NSScrollView, NSViewWidthSizable, \
	NSMutableParagraphStyle
from GUI import export
from GUI import StdFonts
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler
from GUI.GTextEditors import TextEditor as GTextEditor

NUM_TAB_STOPS = 32

class TextEditor(GTextEditor):

	_ns_handle_mouse = True

	def __init__(self, scrolling = 'hv', **kwds):
		width = 100
		height = 100
		frame = ((0, 0), (width,  height))
		ns_outer = NSScrollView.alloc().initWithFrame_(frame)
		ns_outer.setHasHorizontalScroller_('h' in scrolling)
		ns_outer.setHasVerticalScroller_('v' in scrolling)
		if 'h' in scrolling:
			cwidth = 2000
		else:
			cwidth = ns_outer.contentSize()[0]
		frame = ((0, 0), (cwidth,  height))
		ns_inner = PyGUI_NSTextView.alloc().initWithFrame_(frame)
		ns_inner.pygui_component = self
		ps = NSMutableParagraphStyle.alloc().init()
		ps.setDefaultTabInterval_(ps.tabStops()[0].location())
		ps.setTabStops_([])
		ns_inner.setDefaultParagraphStyle_(ps)
		ns_inner.setAllowsUndo_(True)
		ns_outer.setDocumentView_(ns_inner)
		if 'h' not in scrolling:
			ns_inner.setAutoresizingMask_(NSViewWidthSizable)
		if 'font' not in kwds:
			kwds['font'] = StdFonts.application_font
		GTextEditor.__init__(self, ns_outer,
			_ns_inner_view = ns_inner, **kwds)
	
	def get_text(self):
		return self._ns_inner_view.string()
	
	def set_text(self, value):
		self._ns_inner_view.setString_(value)
		self._ns_apply_style()
	
	def get_text_length(self):
		return self._ns_inner_view.textStorage().length()

	def get_selection(self):
		start, length = self._ns_inner_view.selectedRanges()[0].rangeValue()
		return (start, start + length)

	def set_selection(self, value):
		start, stop = value
		self._ns_inner_view.setSelectedRange_((start, stop - start))

	def get_font(self):
		return self._font
	
	def set_font(self, font):
		self._font = font
		self._ns_inner_view.setFont_(font._ns_font)

	def get_tab_spacing(self):
		#ns_storage =  self._ns_inner_view.textStorage()
		#ps, _ = ns_storage.attribute_atIndex_effectiveRange_("NSParagraphStyle", 0)
		ps = self._ns_inner_view.defaultParagraphStyle()
		return ps.defaultTabInterval()

	def set_tab_spacing(self, x):
		ps = NSMutableParagraphStyle.alloc().init()
		ps.setTabStops_([])
		ps.setDefaultTabInterval_(x)
		self._ns_inner_view.setDefaultParagraphStyle_(ps)
		self._ns_apply_style()
	
	def paste_cmd(self):
		GTextEditor.paste_cmd(self)
		self._ns_apply_style()

	def _ns_apply_style(self):
		ns_textview = self._ns_inner_view
		ps = ns_textview.defaultParagraphStyle()
		font = ns_textview.font()
		ns_storage = self._ns_inner_view.textStorage()
		ns_storage.setAttributes_range_(
			{"NSParagraphStyle": ps, "NSFont": font},
			(0, self.text_length))

#------------------------------------------------------------------------------

class PyGUI_NSTextView(NSTextView, PyGUI_NS_EventHandler):
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']

export(TextEditor)
