#
#   Python GUI - Color constants and functions - Gtk
#

from gtk import Style
from GUI import Color

rgb = Color

s = Style()
selection_forecolor = Color._from_gdk_color(s.fg[3])
selection_backcolor = Color._from_gdk_color(s.bg[3])

