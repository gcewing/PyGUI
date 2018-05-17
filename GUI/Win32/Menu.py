#--------------------------------------------------------------------
#
#   PyGUI - Menu - Win32
#
#--------------------------------------------------------------------

import win32ui as ui, win32con as wc
from GUI import export
from GUI.WinMenus import win_command_to_id
from GUI.GMenus import Menu as GMenu

class Menu(GMenu):

	def __init__(self, *args, **kwds):
		GMenu.__init__(self, *args, **kwds)
	
	def _update_platform_menu(self):
		#  Don't need to do anything here because platform menu item
		#  states are updated by HookCommandUpdate handlers.
		pass
	
	def _win_create_menu(self):
		#  Create a fresh platform menu reflecting the current items. Need
		#  to do this because it's not possible to share submenu handles
		#  between windows.
		self._rebuild_platform_menu()
		win_menu = self._win_menu
		self._win_menu = None # So we don't accidentally try to reuse it
		return win_menu
	
	def _clear_platform_menu(self):
		self._win_menu = ui.CreatePopupMenu()

#	def _clear_platform_menu(self):
#		#print "Menu._clear_platform_menu:", self ###
#		bypos = wc.MF_BYPOSITION
#		win_menu = self._win_menu
#		n = win_menu.GetMenuItemCount()
#		for i in xrange(n-1, -1, -1):
#			win_menu.DeleteMenu(i, bypos)
	
	def _add_separator_to_platform_menu(self):
		#print "Menu._add_separator_to_platform_menu:", self ###
		self._win_menu.AppendMenu(wc.MF_SEPARATOR, 0)
	
	def _add_item_to_platform_menu(self, item, name, command_name, *args):
		#print "Menu._add_item_to_platform_menu:", self, item, name ###
		win_text = name.replace("&", "&&")
		key = item._key
		if key:
			win_text += "\tCtrl+"
			if item._shift:
				win_text += "Shift+"
			if item._option:
				win_text += "Alt+"
			win_text += key
		flags = wc.MF_STRING
		#  These are done by HookCommandUpdate handler
		#if not item.enabled:
		#	flags |= wc.MF_GRAYED
		#if item.checked:
		#	flags |= wc.MF_CHECKED
		id = win_command_to_id(command_name, *args)
		self._win_menu.AppendMenu(flags, id, win_text)

export(Menu)
