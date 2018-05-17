#----------------------------------------------------------------------
#
#		Python GUI - Menus - Generic
#
#----------------------------------------------------------------------

from GUI import Globals
from GUI.Properties import Properties, overridable_property

#----------------------------------------------------------------------

def search_list_for_key(items, char, shift, option):
	for i in xrange(len(items)-1, -1, -1):
		result = items[i]._search_for_key(char, shift, option)
		if result:
			return result

#----------------------------------------------------------------------

class Menu(Properties):
	"""Pull-down or pop-up menu class.
	
	Menu(title, item_descriptors)
		constructs a menu with the given title and items. Each
		item_descriptor is of the form
		
			"-"
		
		for a separator,
		
			("text/key", 'command_name')
		
		for a single menu item, or
		
			(["text/key", ...], 'command_name')
	
		for an indexed item group. An indexed group is a group
		of items sharing the same command name and distinguished
		by an integer index. Items can be added to and removed
		from the group dynamically, to implement e.g. a font
		menu or windows menu.
		
		The "key" part of the item descriptor (which is optional)
		specifies the keyboard equivalent. It should consist of
		a single character together with the following optional
		modifiers:
		
			^		representing the Shift key
			@		representing the Alt or Option key
	"""
	
	title = overridable_property('title', "Title string appearing in menu bar")
	special = overridable_property('special', "Menu appears at right end of menu bar")
	
	_flat_items = None

	def __init__(self, title, items, special = False, substitutions = {}, **kwds):
		self._title = title
		self._items = []
		self._special = special
		Properties.__init__(self, **kwds)
		self.extend(items, substitutions)
	
	def get_title(self):
		return self._title
	
	def get_special(self):
		return self._special
	
	def item_with_command(self, cmd):
		for item in self._items:
			if item._command_name == cmd:
				return item
		return None
	
	def append(self, item, substitutions = {}):
		items = self._items
		item = self._make_item(item, substitutions)
		if not (items and isinstance(item, MenuSeparator)
			and isinstance(items[-1], MenuSeparator)):
				items.append(item)
	
	def extend(self, items, substitutions = {}):
		for item in items:
			self.append(item, substitutions)
	
	def _make_item(self, item, substitutions):
		if isinstance(item, MenuItem):
			return item
		elif item == "-":
			return _menu_separator
		else:
			(text, cmd) = item
			if isinstance(text, basestring):
				return SingleMenuItem(text, cmd, substitutions)
			else:
				return MenuItemGroup(text, cmd)
	
	def _command_and_args_for_item(self, item_num):
		i = 1
		for item in self._items:
			n = item._num_subitems()
			if item_num < i + n:
				return item._command_and_args_for_subitem(item_num - i)
			i += n
		return '', ()
	
	def _update_platform_menu(self):
		#  Called during menu setup after items have been enabled/checked.
		#  Generic implementation rebuilds the whole menu from scratch.
		#  Implementations may override this to be more elegant.
		self._rebuild_platform_menu()
	
	def _rebuild_platform_menu(self):
		self._clear_platform_menu()
		for item in self._items:
			item._add_to_platform_menu(self)
	
	def _search_for_key(self, char, shift, option):
		return search_list_for_key(self._items, char, shift, option)
	
	def _get_flat_items(self):
		flat = self._flat_items
		if flat is None:
			flat = []
			for item in self._items:
				item._collect_flat_items(flat)
			self._flat_items = flat
		return flat
	
	def _get_flat_item(self, i):
		return self._get_flat_items()[i]

#----------------------------------------------------------------------

class MenuItem(Properties):
	#	 Internal class representing a menu item, group or separator.
	#
	#  _command_name   string   Internal command name
	
	def _num_subitems(self):
		return 1

	def _split_text(self, text):
		# Split menu text into label and key combination.
		if "/" in text:
			return text.split("/")
		else:
			return text, ""
	
	def _name(self):
		return self._label.replace("<app>", Globals.application_name)
	
	def _collect_flat_items(self, result):
		result.append(self)

#----------------------------------------------------------------------

class MenuSeparator(MenuItem):
	#	 Internal class representing a menu separator.
	
	_command_name = ''
	
	def _add_to_platform_menu(self, menu):
		menu._add_separator_to_platform_menu()

	def _search_for_key(self, char, shift, option):
		pass
	
#----------------------------------------------------------------------

class SingleMenuItem(MenuItem):
	"""Class representing a menu item.
	
	Properties:
		enabled    boolean
		checked    boolean
	"""
	
	enabled = 0
	checked = 0
	_key = None
	_shift = 0
	_option = 0
	#_index = None
	
	def __init__(self, text, cmd, substitutions = {}):
		label1, keycomb1 = self._split_text(text)
		label2, keycomb2 = self._split_text(substitutions.get(cmd, ""))
		self._label = label2 or label1
		keycomb = keycomb2 or keycomb1
		for c in keycomb:
			if c == '^':
				self._shift = 1
			elif c == '@':
				self._option = 1
			else:
				self._key = c.upper()
		self._command_name = cmd
	
	def __str__(self):
		return "<SingleMenuItem %r %r Sh:%s Op:%s En:%s>" % (
			self._label, self._key, self._shift, self._option, self.enabled)
	
	def _add_to_platform_menu(self, menu):
		menu._add_item_to_platform_menu(self, self._name(), self._command_name)
	
	def _command_and_args_for_subitem(self, i):
		return self._command_name, ()

	def _search_for_key(self, char, shift, option):
		if self._matches_key(char, shift, option):
			return self._command_name
	
	def _matches_key(self, char, shift, option):
		return self._key == char and self._shift == shift \
			and self._option == option and self.enabled

#----------------------------------------------------------------------

class MenuItemGroup(MenuItem):
	"""Class representing a menu item group.
	
	Properties:
		enabled  <-  boolean     Assigning to these changes the corresponding
		checked  <-  boolean     property of all the group's items.
	
	Operators:
		group[index]  ->  MenuItem 
	
	Methods:
		set_items(["text/key", ...])
			Replaces all the items in the group by the specified items.
	"""
	
	enabled = overridable_property('enabled')
	checked = overridable_property('checked')
		
	def __init__(self, text_list, cmd):
		self.set_items(text_list)
		self._command_name = cmd
	
	def _num_subitems(self):
		return len(self._items)
	
	def _command_and_args_for_subitem(self, i):
		return self._command_name, (i,)
	
	def get_enabled(self):
		raise AttributeError("'enabled' property of MenuItemGroup is write-only")
	
	def set_enabled(self, state):
		for item in self._items:
			item.enabled = state
	
	def get_checked(self):
		raise AttributeError("'checked' property of MenuItemGroup is write-only")
	
	def set_checked(self, state):
		for item in self._items:
			item.checked = state
	
	def __getitem__(self, index):
		return self._items[index]
	
	def set_items(self, text_list):
		self._items = [SingleMenuItem(text, '') for text in text_list]
	
	def _add_to_platform_menu(self, menu):
		#for item in self._items:
		#	item._add_to_platform_menu(menu)
		cmd = self._command_name
		for index, item in enumerate(self._items):
			menu._add_item_to_platform_menu(item, item._name(), cmd, index)

	def _search_for_key(self, char, shift, option):
		items = self._items
		for i in xrange(len(items)-1, -1, -1):
			if items[i]._matches_key(char, shift, option):
				return (self._command_name, i)

	def _collect_flat_items(self, result):
		for item in self._items:
			item._collect_flat_items(result)

#----------------------------------------------------------------------

_menu_separator = MenuSeparator()
_dummy_menu_item = SingleMenuItem("", '')

#----------------------------------------------------------------------

class MenuState:
	"""A MenuState object is used to enable/disable and check/uncheck
	menu items, and to add or remove items of indexed groups,
	during the menu setup phase of menu command handling.
	
	Each single menu item or item group appears as an attribute of
	the MenuState object, with the command name as the attribute name,
	allowing operations such as
	
		menu_state.copy_cmd.enabled = 1
		menu_state.font_cmd[current_font].checked = 1
	
	The command name may also be used as a mapping index.
	
	Operators:
		menu_state.command_name	 ->	 MenuItem
		menu_state['command_name']	 ->	 MenuItem
	"""

	def __init__(self, menu_list):
		mapping = {}
		for menu in menu_list:
			for item in menu._items:
				cmd = item._command_name
				if cmd:
					mapping[cmd] = item
		self._mapping = mapping
	
	def __getattr__(self, name):
		try:
			return self._mapping[name]
		except KeyError:
			if name.startswith("__"):
				raise AttributeError, name
			return _dummy_menu_item
	
	__getitem__ = __getattr__

	def reset(self):
		"""Disable and uncheck all items."""
		for item in self._mapping.values():
			item.enabled = 0
			item.checked = None
