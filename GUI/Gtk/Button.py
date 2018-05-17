#
#   Python GUI - Buttons - Gtk version
#

import gtk
from GUI import export
from GUI.StdFonts import system_font
from GUI.GButtons import Button as GButton

_gtk_extra_hpad = 5   # Amount to add to default width at each end
_gtk_icon_spacing = 2  # Space to leave between icon and label

class Button(GButton):

	_gtk_icon = None    # Icon, when we have one
	_style = 'normal'   # or 'default' or 'cancel'
	
	def __init__(self, title = "Button", #style = 'normal',
			font = system_font, **kwds):
		gtk_label = gtk.Label(title)
		gtk_box = gtk.HBox(spacing = _gtk_icon_spacing)
		gtk_box.pack_end(gtk_label, fill = True, expand = True)
		gtk_alignment = gtk.Alignment(0.5, 0.5, 0.0, 0.0)
		hp = _gtk_extra_hpad
		gtk_alignment.set_padding(0, 0, hp, hp)
		gtk_alignment.add(gtk_box)
		gtk_button = gtk.Button()
		gtk_button.add(gtk_alignment)
		gtk_button.set_focus_on_click(False)
		gtk_button.show_all()
		w, h = font.text_size(title)
		w2 = w + 2 * _gtk_button_hpad + _gtk_icon_width + _gtk_icon_spacing
		h2 = max(h + 2 * _gtk_button_vpad, _gtk_default_button_height)
		gtk_button.set_size_request(int(round(w2)), int(round(h2)))
		self._gtk_box = gtk_box
		self._gtk_alignment = gtk_alignment
		self._gtk_connect(gtk_button, 'clicked', self._gtk_clicked_signal)
		GButton.__init__(self, _gtk_outer = gtk_button, _gtk_title = gtk_label,
			font = font, **kwds)
	
	def _gtk_get_alignment(self):
		return self._gtk_alignment.get_property('xalign')
	
	def _gtk_set_alignment(self, fraction, just):
		self._gtk_alignment.set_property('xalign', fraction)
		self._gtk_title_widget.set_justify(just)
	
	def get_style(self):
		return self._style
	
	def set_style(self, new_style):
		if self._style <> new_style:
			if new_style == 'default':
				self._gtk_add_icon(gtk.STOCK_OK)
			elif new_style == 'cancel':
				self._gtk_add_icon(gtk.STOCK_CANCEL)
			else:
				self._gtk_remove_icon()
		self._style = new_style
	
	def _gtk_add_icon(self, gtk_stock_id):
		gtk_icon = gtk.image_new_from_stock(gtk_stock_id, gtk.ICON_SIZE_BUTTON)
		gtk_icon.show()
		self._gtk_box.pack_start(gtk_icon)
		self._gtk_icon = gtk_icon

	def _gtk_remove_icon(self):
		gtk_icon = self._gtk_icon
		if gtk_icon:
			gtk_icon.destroy()
			self._gtk_icon = None
	
	def activate(self):
		"""Highlight the button momentarily and then perform its action."""
		self._gtk_outer_widget.activate()
	
	def _gtk_clicked_signal(self):
		self.do_action()


def _calc_size_constants():
	global _gtk_icon_width, _gtk_default_button_height
	global _gtk_button_hpad, _gtk_button_vpad
	gtk_icon = gtk.image_new_from_stock(gtk.STOCK_OK, gtk.ICON_SIZE_BUTTON)
	gtk_button = gtk.Button()
	gtk_button.add(gtk_icon)
	gtk_button.show_all()
	icon_width, icon_height = gtk_icon.size_request()
	butn_width, butn_height = gtk_button.size_request()
	_gtk_icon_width = icon_width
	_gtk_default_button_height = butn_height
	_gtk_button_hpad = (butn_width - icon_width) / 2 + _gtk_extra_hpad
	_gtk_button_vpad = (butn_height - icon_height) / 2
	gtk_button.destroy()

_calc_size_constants()
del _calc_size_constants

export(Button)

