#
#		Python GUI - Standard Fonts - Gtk
#

import gtk
from GUI import Font

system_font = Font._from_pango_description(gtk.Label().style.font_desc)
application_font = Font._from_pango_description(gtk.Entry().style.font_desc)
