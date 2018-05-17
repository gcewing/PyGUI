#
#		Python GUI - Menus - PyObjC
#

from AppKit import NSMenu, NSMenuItem, NSOnState, \
	NSCommandKeyMask, NSShiftKeyMask, NSAlternateKeyMask
from GUI import export
from GUI import Globals
from GUI.GMenus import Menu as GMenu, MenuItem

#_ns_standard_actions = {
#	'undo_cmd': 'undo:',
#	'redo_cmd': 'redo:',
#	'cut_cmd': 'cut:',
#	'copy_cmd': 'copy:',
#	'paste_cmd': 'paste:',
#	'clear_cmd': 'clear:',
#	'select_all_cmd': 'selectAll:',
#}

class Menu(GMenu):

	def __init__(self, title, items, **kwds):
		#print "Menu: creating with items", items ###
		GMenu.__init__(self, title, items, **kwds)
		ns_menu = NSMenu.alloc().initWithTitle_(title)
		ns_menu.setAutoenablesItems_(False)
		ns_menu.setDelegate_(Globals.ns_application)
		self._ns_menu = ns_menu
	
	def _clear_platform_menu(self):
		ns_menu = self._ns_menu
		n = ns_menu.numberOfItems()
		while n:
			n -= 1
			ns_menu.removeItemAtIndex_(n)
	
	def _add_separator_to_platform_menu(self):
		ns_item = NSMenuItem.separatorItem()
		self._ns_menu.addItem_(ns_item)
	
	def _add_item_to_platform_menu(self, item, name, command = None, index = None):
		key = item._key or ""
		if item._shift:
			key = key.upper()
		else:
			key = key.lower()
		ns_item = NSMenuItem.alloc()
		#ns_action = _ns_standard_actions.get(command, 'menuSelection:')
		ns_action = 'menuSelection:'
		ns_item.initWithTitle_action_keyEquivalent_(name, ns_action, key)
		ns_item.setEnabled_(item.enabled)
		if item.checked:
			ns_item.setState_(NSOnState)
		ns_modifiers = NSCommandKeyMask
		if item._option:
			ns_modifiers |= NSAlternateKeyMask
		ns_item.setKeyEquivalentModifierMask_(ns_modifiers)
		ns_item.setRepresentedObject_(command)
		if index is not None:
			ns_tag = index
		else:
			ns_tag = -1
		ns_item.setTag_(ns_tag)
		self._ns_menu.addItem_(ns_item)

export(Menu)
