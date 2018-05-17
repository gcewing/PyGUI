#
#   Python GUI - Alert base class - Gtk
#

import gtk
from GUI import export
from GUI.GBaseAlerts import BaseAlert as GBaseAlert

_kind_to_gtk_stock_id = {
	'stop':    gtk.STOCK_DIALOG_ERROR,
	'caution': gtk.STOCK_DIALOG_WARNING,
	'note':    gtk.STOCK_DIALOG_INFO,
	'query':   gtk.STOCK_DIALOG_QUESTION,
}

class BaseAlert(GBaseAlert):

	def _layout_icon(self, kind):
		gtk_stock_id = _kind_to_gtk_stock_id[kind]
		gtk_icon = gtk.image_new_from_stock(gtk_stock_id, gtk.ICON_SIZE_DIALOG)
		gtk_icon.show()
		icon_size = gtk_icon.size_request()
		icon_width, icon_height = icon_size
		self._gtk_inner_widget.put(gtk_icon, self._left_margin, self._top_margin)
		return icon_size

export(BaseAlert)
