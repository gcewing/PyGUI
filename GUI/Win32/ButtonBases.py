#--------------------------------------------------------------------
#
#   PyGUI - Button base - Win32
#
#--------------------------------------------------------------------

class ButtonBase(object):

	def key_down(self, event):
		if not event.auto:
			c = event.char
			if c == ' ' or c == '\r':
				self._win.SetState(True)
			else:
				#GControl.key_down(self, event)
				super(ButtonBase, self).key_down(event)
	
	def key_up(self, event):
		c = event.char
		if c == ' ' or c == '\r':
			if self._win.GetState() & 4:
				self._win.SetState(False)
				self._win_activate()
		else:
			#GControl.key_up(self, event)
			super(ButtonBase, self).key_up(event)

