#
#   Python GUI - Alert base class - Gtk
#

from gi.repository import Gtk
from GUI.GBaseAlerts import BaseAlert as GBaseAlert

_kind_to_gtk_stock_id = {
	'stop':    Gtk.STOCK_DIALOG_ERROR,
	'caution': Gtk.STOCK_DIALOG_WARNING,
	'note':    Gtk.STOCK_DIALOG_INFO,
	'query':   Gtk.STOCK_DIALOG_QUESTION,
}

class BaseAlert(GBaseAlert):

	def _layout_icon(self, kind):
		gtk_stock_id = _kind_to_gtk_stock_id[kind]
		gtk_icon = Gtk.Image.new_from_stock(gtk_stock_id, Gtk.IconSize.DIALOG)
		gtk_icon.show()
		icon_size = gtk_icon.size_request()
		self._gtk_inner_widget.put(gtk_icon, self._left_margin, self._top_margin)
		return icon_size.width, icon_size.height

