#
#		Python GUI - Frames - Gtk
#

from gtk import Fixed
from GUI import export
from GUI.GFrames import Frame as GFrame

class Frame(GFrame):

	def __init__(self, **kwds):
		gtk_widget = Fixed()
		gtk_widget.show()
		GFrame.__init__(self, _gtk_outer = gtk_widget)

export(Frame)
