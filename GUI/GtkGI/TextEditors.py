#
#   Python GUI - Text Editor - Gtk
#

import pango, gtk
from GUI.Globals import application
from GUI.GTextEditors import TextEditor as GTextEditor
from GUI.Scrollables import Scrollable
from GUI.Fonts import Font

class TextEditor(GTextEditor, Scrollable):

	_font = None

	def __init__(self, scrolling = 'hv', **kwds):
		gtk_sw = Gtk.ScrolledWindow()
		gtk_sw.show()
		gtk_tv = Gtk.TextView()
		gtk_tv.show()
		gtk_sw.add(gtk_tv)
		gtk_tb = Gtk.TextBuffer()
		self._gtk_textbuffer = gtk_tb
		gtk_tv.set_buffer(self._gtk_textbuffer)
		tag = Gtk.TextTag()
		tabs = Pango.TabArray(1, True)
		tabs.set_tab(0, Pango.TabAlign.LEFT, 28)
		tag.set_property('tabs', tabs)
		tag.set_property('tabs-set', True)
		self._gtk_tag = tag
		gtk_tb.get_tag_table().add(tag)
		GTextEditor.__init__(self, _gtk_outer = gtk_sw, _gtk_inner = gtk_tv,
			_gtk_focus = gtk_tv, **kwds)
		self.set_hscrolling('h' in scrolling)
		self.set_vscrolling('v' in scrolling)
		if 'h' not in scrolling:
			gtk_tv.set_wrap_mode(Gtk.WrapMode.WORD)
		self._gtk_apply_tag()

	def _gtk_get_sel_iters(self):
		gtk_textbuffer = self._gtk_textbuffer
		sel_iters = gtk_textbuffer.get_selection_bounds()
		if not sel_iters:
			insert_mark = gtk_textbuffer.get_insert()
			insert_iter = gtk_textbuffer.get_iter_at_mark(insert_mark)
			sel_iters = (insert_iter, insert_iter)
		return sel_iters
	
	def _gtk_apply_tag(self):
		tb = self._gtk_textbuffer
		tb.apply_tag(self._gtk_tag, tb.get_start_iter(), tb.get_end_iter())
	
	def get_selection(self):
		tb = self._gtk_textbuffer
		bounds = tb.get_selection_bounds()
		if bounds:
			return (bounds[0].get_offset(), bounds[1].get_offset())
		else:
			i = tb.get_property('cursor-position')
			return (i, i)

	def set_selection(self, value):
		tb = self._gtk_textbuffer
		start = tb.get_iter_at_offset(value[0])
		end = tb.get_iter_at_offset(value[1])
		tb.select_range(start, end)

	def get_text(self):
		tb = self._gtk_textbuffer
		start = tb.get_start_iter()
		end = tb.get_end_iter()
		return tb.get_slice(start, end)

	def set_text(self, text):
		self._gtk_textbuffer.set_text(text)
		self._gtk_apply_tag()
	
	def get_text_length(self):
		return self._gtk_textbuffer.get_end_iter().get_offset()

	def get_font(self):
		font = self._font
		if not font:
			font = Font._from_pango_description(self._gtk_inner_widget.style.font_desc)
		return font
		
	def set_font(self, f):
		self._font = f
		tv = self._gtk_inner_widget
		tv.modify_font(f._pango_description)
	
	def get_tab_spacing(self):
		tabs = self._gtk_tag.get_property('tabs')
		return tabs.get_tab(0)[1]
	
	def set_tab_spacing(self, x):
		tabs = Pango.TabArray(1, True)
		tabs.set_tab(0, Pango.TabAlign.LEFT, x)
		self._gtk_tag.set_property('tabs', tabs)

	def cut_cmd(self):
		self.copy_cmd()
		self.clear_cmd()
	
	def copy_cmd(self):
		gtk_textbuffer = self._gtk_textbuffer
		start_iter, end_iter = self._gtk_get_sel_iters()
		text = gtk_textbuffer.get_text(start_iter, end_iter, 1)
		if text:
			application().set_clipboard(text)
	
	def paste_cmd(self):
		text = application().get_clipboard()
		self.clear_cmd()
		self._gtk_textbuffer.insert_at_cursor(text)
	
	def clear_cmd(self):
		gtk_textbuffer = self._gtk_textbuffer
		start_iter, end_iter = self._gtk_get_sel_iters()
		gtk_textbuffer.delete(start_iter, end_iter)
