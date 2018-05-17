#
#		Python GUI - Menu Lists - Generic
#

from GUI import export

class MenuList(list):
	"""A MenuList is a sequence of Menus with methods for finding
	menus and menu items by command."""
	
	def menu_with_command(self, cmd):
		"""Returns the menu containing the given command, or None
		if there is no such menu in the list."""
		for menu in self:
			if menu.item_with_command(cmd):
				return menu
		return None
	
	def item_with_command(self, cmd):
		"""Returns the menu item having the given command, or None
		if there is no such item."""
		for menu in self:
			item = menu.item_with_command(cmd)
			if item:
				return item
		return None

export(MenuList)
