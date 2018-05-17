#
#   PyGUI - Edit command handling - Cocoa
#

from AppKit import NSMenuItem
from GUI import export

class EditCmdHandler(object):
	#  Mixin for Components whose _ns_responder handles the
	#  standard editing commands.
	
	def setup_menus(self, m):
		def validate(cmd_name, ns_selector):
			ns_menu_item = NSMenuItem.alloc().\
				initWithTitle_action_keyEquivalent_("", ns_selector, "")
			m[cmd_name].enabled = ns_target.validateMenuItem_(ns_menu_item)
		ns_target = self.window._ns_window
		if ns_target:
			validate('undo_cmd', 'undo:')
			validate('redo_cmd', 'redo:')
		ns_target = self._ns_edit_cmd_target()
		if ns_target:
			validate('cut_cmd', 'cut:')
			validate('copy_cmd', 'copy:')
			validate('paste_cmd', 'paste:')
			validate('clear_cmd', 'delete:')
			validate('select_all_cmd', 'selectAll:')
	
	def undo_cmd(self):
		ns_window = self.window._ns_window
		if ns_window:
			ns_window.undo_(None)
	
	def redo_cmd(self):
		ns_window = self.window._ns_window
		if ns_window:
			ns_window.redo_(None)
	
	def cut_cmd(self):
		self._ns_edit_cmd('cut_')
	
	def copy_cmd(self):
		self._ns_edit_cmd('copy_')
	
	def paste_cmd(self):
		self._ns_edit_cmd('paste_')
	
	def clear_cmd(self):
		self._ns_edit_cmd('delete_')
	
	def select_all_cmd(self):
		self._ns_edit_cmd('selectAll_')
	
	def _ns_edit_cmd(self, ns_method_name):
		ns_target = self._ns_edit_cmd_target()
		if ns_target:
			getattr(ns_target, ns_method_name)(None)
	
	def _ns_edit_cmd_target(self):
		return self._get_ns_responder()

export(EditCmdHandler)
