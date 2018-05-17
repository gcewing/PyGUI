#
#   Python GUI - Text fields - Gtk
#

import gtk
from GUI import export
from GUI.Properties import overridable_property
from GUI import application
from GUI.StdFonts import application_font
from GUI.GTextFields import TextField as GTextField

gtk_margins = (2, 2, 0, 0)

class TextField(GTextField):
	
	_pass_key_events_to_platform = True

	_multiline = 0
	_gtk_setting_text = False
	
	def __init__(self, font = application_font, lines = 1, 
			multiline = 0, password = 0, **kwds):
		self._multiline = multiline
		lm, tm, rm, bm = gtk_margins
		if multiline:
			gtk_textbuffer = gtk.TextBuffer()
			gtk_textview = gtk.TextView(gtk_textbuffer)
			#gtk_textview.set_accepts_tab(False) #^%$#^%$!!! moves the focus itself.
			#self._gtk_connect(gtk_textview, 'key-press-event', self._gtk_key_press_event)
			self._gtk_connect(gtk_textbuffer, 'changed', self._gtk_changed)
			gtk_alignment = gtk.Alignment(0.5, 0.5, 1.0, 1.0)
			gtk_alignment.set_padding(tm, bm, lm, rm)
			gtk_alignment.add(gtk_textview)
			gtk_box = gtk.EventBox()
			gtk_box.add(gtk_alignment)
			gtk_box.modify_bg(gtk.STATE_NORMAL,
				gtk_textview.style.base[gtk.STATE_NORMAL])
			gtk_frame = gtk.Frame()
			gtk_frame.set_shadow_type(gtk.SHADOW_IN)
			gtk_frame.add(gtk_box)
			self._gtk_textbuffer = gtk_textbuffer
			gtk_text_widget = gtk_textview
			gtk_outer = gtk_frame
		else:
			gtk_entry = gtk.Entry()
			#self._gtk_connect(gtk_entry, 'key-press-event', self._gtk_key_press_event)
			self._gtk_connect(gtk_entry, 'changed', self._gtk_changed)
			self._gtk_entry = gtk_entry
			gtk_text_widget = gtk_entry
			gtk_outer = gtk_entry
		self._gtk_text_widget = gtk_text_widget
		self._font = font
		gtk_text_widget.modify_font(font._pango_description)
		self._vertical_padding = tm + 2 * gtk_outer.style.ythickness + bm
		height = self._vertical_padding + lines * font.text_size("X")[1]
		gtk_outer.set_size_request(-1, height)
		self._password = password
		if password:
			if not multiline:
				self._gtk_entry.set_visibility(0)
				self._gtk_entry.set_invisible_char("*")
			else:
				raise ValueError("The password option is not supported for multiline"
					" TextFields on this platform")
		gtk_outer.show_all()
		GTextField.__init__(self,
			_gtk_outer = gtk_outer,
			_gtk_title = gtk_text_widget,
			_gtk_focus = gtk_text_widget,
			_gtk_input = gtk_text_widget,
			multiline = multiline, **kwds)
	
	def get_text(self):
		if self._multiline:
			gtk_textbuffer = self._gtk_textbuffer
			start = gtk_textbuffer.get_start_iter()
			end = gtk_textbuffer.get_end_iter()
			return self._gtk_textbuffer.get_text(start, end, 1)
		else:
			return self._gtk_entry.get_text()
	
	def set_text(self, text):
		self._gtk_setting_text = True
		try:
			if self._multiline:
				self._gtk_textbuffer.set_text(text)
			else:
				self._gtk_entry.set_text(text)
		finally:
			self._gtk_setting_text = False
	
	def get_selection(self):
		if self._multiline:
			gtk_textbuffer = self._gtk_textbuffer
			start_iter, end_iter = self._gtk_get_sel_iters()
			start = start_iter.get_offset()
			end = end_iter.get_offset()
			sel = (start, end)
		else:
			sel = self._gtk_get_sel_positions()
		return sel
	
	def _gtk_get_sel_iters(self):
		gtk_textbuffer = self._gtk_textbuffer
		sel_iters = gtk_textbuffer.get_selection_bounds()
		if not sel_iters:
			insert_mark = gtk_textbuffer.get_insert()
			insert_iter = gtk_textbuffer.get_iter_at_mark(insert_mark)
			sel_iters = (insert_iter, insert_iter)
		return sel_iters
	
	def _gtk_get_sel_positions(self):
		gtk_entry = self._gtk_entry
		sel = gtk_entry.get_selection_bounds()
		if not sel:
			pos = gtk_entry.get_position()
			sel = (pos, pos)
		return sel
	
	def _set_selection(self, start, end):
		if self._multiline:
			gtk_textbuffer = self._gtk_textbuffer
			start_iter = gtk_textbuffer.get_iter_at_offset(start)
			end_iter = gtk_textbuffer.get_iter_at_offset(end)
			gtk_textbuffer.select_range(start_iter, end_iter)
		else:
			self._gtk_entry.select_region(start, end)

	def set_selection(self, (start, end)):
		self._set_selection(start, end)
		self.become_target()
	
	def get_multiline(self):	
		return self._multiline
	
	def get_password(self):
		return self._password
	
	def _select_all(self):
		if self._multiline:
			gtk_textbuffer = self._gtk_textbuffer
			start = gtk_textbuffer.get_start_iter()
			end = gtk_textbuffer.get_end_iter()
			gtk_textbuffer.select_range(start, end)
		else:
			self._gtk_entry.select_region(0, -1)

	def select_all(self):
		self._select_all()
		self.become_target()

	def cut_cmd(self):
		self.copy_cmd()
		self.clear_cmd()
	
	def copy_cmd(self):
		if self._password:
			return
		if self._multiline:
			gtk_textbuffer = self._gtk_textbuffer
			start_iter, end_iter = self._gtk_get_sel_iters()
			text = gtk_textbuffer.get_text(start_iter, end_iter, 1)
		else:
			start, end = self._gtk_get_sel_positions()
			text = self._gtk_entry.get_chars(start, end)
		if text:
			application().set_clipboard(text)
	
	def paste_cmd(self):
		text = application().get_clipboard()
		self.clear_cmd()
		if self._multiline:
			self._gtk_textbuffer.insert_at_cursor(text)
		else:
			gtk_entry = self._gtk_entry
			pos = gtk_entry.get_position()
			gtk_entry.insert_text(text, pos)
			gtk_entry.set_position(pos + len(text))
	
	def clear_cmd(self):
		if self._multiline:
			gtk_textbuffer = self._gtk_textbuffer
			start_iter, end_iter = self._gtk_get_sel_iters()
			gtk_textbuffer.delete(start_iter, end_iter)
		else:
			start, end = self._gtk_get_sel_positions()
			self._gtk_entry.delete_text(start, end)
	
	def _untargeted(self):
		self._set_selection(0, 0)
	
	def _tab_in(self):
		self._select_all()
		GTextField._tab_in(self)
	
	def _gtk_changed(self):
		if not self._gtk_setting_text:
			#print("TextField._gtk_changed")
			self.do_text_changed_action()

	def get_editable(self):
		return self._gtk_text_widget.get_property("editable")
	
	def set_editable(self, x):
		self._gtk_text_widget.set_property("editable", x)

export(TextField)
