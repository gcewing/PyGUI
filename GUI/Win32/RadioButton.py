#--------------------------------------------------------------------
#
#   PyGUI - RadioButton - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI import export
from GUI.StdFonts import system_font
from GUI.ButtonBases import ButtonBase
from GUI.GRadioButtons import RadioButton as GRadioButton

win_check_size = 13
win_hpad = 5

class RadioButton(ButtonBase, GRadioButton):

	#_win_transparent = True
	
	def __init__(self, title = "New Radio Button", **kwds):
		font = self._win_predict_font(kwds)
		w = font.width(title) + win_hpad + win_check_size
		h = max(self._calc_height(font), win_check_size)
		win_style = wc.BS_RADIOBUTTON
		win = self._win_create_button(title, win_style, w, h)
		GRadioButton.__init__(self, _win = win, **kwds)
	
	def _value_changed(self):
		self._win_update()

	def _win_update(self):
		group = self._group
		if group:
			state = self._value == group._value
		else:
			state = False
		self._win.SetCheck(state)

#  Unbelievably, a BN_CLICKED message is sent when the
#  button is focused, making it impossible to tell whether
#  it was clicked or tabbed into.
#
#	def _win_bn_clicked(self):
#		print "RadioButton._win_bn_clicked" ###
#		self._win_activate()

	def _win_activate(self):
		group = self._group
		if group:
			group.value = self._value

	def mouse_up(self, event):
		if self._win.GetState() & 0x4: # highlight
			self._win_activate()
		GRadioButton.mouse_up(self, event)

export(RadioButton)
