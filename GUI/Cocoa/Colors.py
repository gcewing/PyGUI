#
#   Python GUI - Color constants and functions - Cocoa
#

from AppKit import NSColor
from GUI import Color

rgb = Color

selection_forecolor = Color._from_ns_color(NSColor.selectedTextColor())
selection_backcolor = Color._from_ns_color(NSColor.selectedTextBackgroundColor())
