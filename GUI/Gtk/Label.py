#
#   Python GUI - Labels - Gtk
#

import gtk
from GUI import export
from GUI.StdFonts import system_font
from GUI.GLabels import Label as GLabel

class Label(GLabel):

	_vertical_padding = 6
	
	def __init__(self, text = "New Label", font = system_font, **kwds):
		width, height = font.text_size(text)
		gtk_label = gtk.Label(text)
		gtk_label.set_alignment(0.0, 0.5)
		gtk_label.set_size_request(width, height + self._vertical_padding)
		gtk_label.show()
		GLabel.__init__(self, _gtk_outer = gtk_label, font = font, **kwds)

	def get_text(self):
		return self._gtk_outer_widget.get_text()
	
	def set_text(self, text):
		self._gtk_outer_widget.set_text(text)
	
	def _gtk_get_alignment(self):
		return self._gtk_outer_widget.get_alignment()[0]
	
	def _gtk_set_alignment(self, fraction, just):
		gtk_label = self._gtk_outer_widget
		gtk_label.set_alignment(fraction, 0.0)
		gtk_label.set_justify(just)

export(Label)
