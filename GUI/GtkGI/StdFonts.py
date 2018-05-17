#
#		Python GUI - Standard Fonts - Gtk
#

from gi.repository import Gtk
from GUI.Fonts import Font

system_font = Font._from_pango_description(Gtk.Label().get_style().font_desc)
application_font = Font._from_pango_description(Gtk.Entry().get_style().font_desc)
