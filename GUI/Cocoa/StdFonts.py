#
#		Python GUI - Standard Fonts - PyObjC
#

from AppKit import NSFont
from GUI import Font

system_font = Font._from_ns_font(NSFont.systemFontOfSize_(0))
application_font = Font._from_ns_font(NSFont.userFontOfSize_(0))
