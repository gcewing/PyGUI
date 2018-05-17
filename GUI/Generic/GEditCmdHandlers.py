#
#   PyGUI - Edit command handling - Generic
#

from GUI import application

class EditCmdHandler(object):
	#  Mixin for objects that implement the standard editing commands.
	
	_may_be_password = False
	
	def setup_menus(self, m):
		selbeg, selend = self.selection
		anysel = selbeg < selend
		anyscrap = application().query_clipboard()
		passwd = self._may_be_password and self.password
		m.cut_cmd.enabled = anysel and not passwd
		m.copy_cmd.enabled = anysel and not passwd
		m.paste_cmd.enabled = anyscrap
		m.clear_cmd.enabled = anysel
		m.select_all_cmd.enabled = True
	
	def select_all_cmd(self):
		self.select_all()

	def select_all(self):
		self.selection = (0, self.get_text_length())

