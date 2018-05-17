#--------------------------------------------------------------------------
#
#		Python GUI - Cursors - Win32
#
#--------------------------------------------------------------------------

import win32gui as gui
from GUI import export
from GUI.GCursors import Cursor as GCursor

class Cursor(GCursor):

	def _from_win_cursor(cls, hcursor):
		cursor = cls.__new__(cls)
		cursor._win_cursor = hcursor
		return cursor

	_from_win_cursor = classmethod(_from_win_cursor)

	def __str__(self):
		return "<Cursor hcursor=0x%x>" % self._win_cursor

	def _init_from_image_and_hotspot(self, image, hotspot):
		#print "Cursor._init_from_image_and_hotspot:" ###
		hicon = image._win_image.GetHICON()
		iconinfo = gui.GetIconInfo(hicon)
		gui.DestroyIcon(hicon)
		flag, xhot, yhot, hbmMask, hbmColor = iconinfo
		xhot, yhot = hotspot
		cursorinfo = (True, xhot, yhot, hbmMask, hbmColor)
		win_cursor = gui.CreateIconIndirect(cursorinfo)
		gui.DeleteObject(hbmMask)
		gui.DeleteObject(hbmColor)
		self._win_cursor = win_cursor

export(Cursor)
