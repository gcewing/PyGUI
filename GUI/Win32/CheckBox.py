#--------------------------------------------------------------------
#
#   PyGUI - CheckBox - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui
from GUI import export
from GUI.StdFonts import system_font
from GUI.ButtonBases import ButtonBase
from GUI.GCheckBoxes import CheckBox as GCheckBox

win_check_size = 13
win_hpad = 5

win_styles = (
	[wc.BS_CHECKBOX, wc.BS_AUTOCHECKBOX],
	[wc.BS_3STATE, wc.BS_AUTO3STATE],
)

win_states = (
	[False, True],
	[False, True, 'mixed'],
)

class CheckBox(ButtonBase, GCheckBox):

	#_win_transparent = True
	
	def __init__(self, title = "New Checkbox", **kwds):
		font = self._win_predict_font(kwds)
		self._auto_toggle = kwds.pop('auto_toggle', True)
		self._mixed = kwds.get('mixed', False)
		w = font.width(title) + win_hpad + win_check_size
		h = max(self._calc_height(font), win_check_size)
		win_style = self._win_button_style()
		win = self._win_create_button(title, win_style, w, h)
		GCheckBox.__init__(self, _win = win, **kwds)
	
	def get_auto_toggle(self):
		return win_styles[self._mixed].index(self._win.GetButtonStyle()) != 0

	def set_auto_toggle(self, x):
		self._auto_toggle = bool(x)
		self._win_update_button_style()
	
	def set_mixed(self, v):
		GCheckBox.set_mixed(self, v)
		self._win_update_button_style()

	def get_on(self):
		return win_states[self._mixed][self._win.GetCheck() & 0x3]
	
	def set_on(self, x):
		try:
			state = win_states[self._mixed].index(x)
		except ValueError:
			raise ValueError("Invalid CheckBox state '%s'" % x)
		self._win.SetCheck(state)
	
	def _win_update_button_style(self):
		self._win.SetButtonStyle(self._win_button_style())
	
	def _win_button_style(self):
		return win_styles[self._mixed][self._auto_toggle]

	def _win_bn_clicked(self):
		#print "CheckBox._win_bn_clicked:", self ###
		self.do_action()

	def _win_activate(self):
		if self.auto_toggle:
			states = win_states[self._mixed]
			i = states.index(self.on)
			self.on = states[(i+1) % len(states)]
		self.do_action()

export(CheckBox)
