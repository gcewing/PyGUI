#--------------------------------------------------------------------
#
#   PyGUI - Button - Win32
#
#--------------------------------------------------------------------

from time import sleep
import win32con as wc, win32ui as ui, win32gui as gui
from GUI import export
from GUI.ButtonBases import ButtonBase
from GUI.GButtons import Button as GButton

win_hpad = 40

win_style_map = {
	'normal': wc.BS_PUSHBUTTON,
	'default': wc.BS_DEFPUSHBUTTON,
	'cancel': wc.BS_PUSHBUTTON,
}

def win_style(style):
	try:
		return win_style_map[style]
	except KeyError:
		raise ValueError("Invalid Button style %r" % style)

#--------------------------------------------------------------------

class Button(ButtonBase, GButton):

	_vertical_padding = 10

	_color = None

	def __init__(self, title = "New Button", **kwds):
		font = self._win_predict_font(kwds)
		style = kwds.pop('style', 'normal')
		self._style = style
		w = font.width(title) + win_hpad
		h = self._calc_height(font)
		win = self._win_create_button(title, win_style(style), w, h)
		GButton.__init__(self, _win = win, **kwds)

	def get_style(self):
		return self._style
	
	def set_style(self, x):
		self._style = x
		self._win.SetButtonStyle(win_style(x))
		
	def flash(self):
		win = self._win
		win.SetState(True)
		sleep(0.05)
		win.SetState(False)
	
	def _win_bn_clicked(self):
		self.do_action()

	def _win_activate(self):
		self.do_action()

export(Button)