#-------------------------------------------------------------------------------
#
#   PyGUI - Standard Menus - Generic
#
#-------------------------------------------------------------------------------

from GUI.Compatibility import set
from GUI import Menu
from GUI import MenuList

#-------------------------------------------------------------------------------

class CommandSet(set):
	"""A set of menu command names.
	
	Constructors:
		CommandSet(string)
		CommandSet(sequence of strings)
	
	Operations:
		string in CommandSet
		CommandSet + x
		CommmandSet - x
		x + CommandSet
		x - CommandSet
		CommandSet += x
		CommandSet -= x
		where x is a CommandSet, a string or a sequence of strings
	"""

	def __init__(self, arg = None):
		if arg:
			if isinstance(arg, basestring):
				arg = [arg]
			set.__init__(self, arg)

	def __or__(self, other):
		return as_command_set(set.__or__(self, as_command_set(other)))

	__ror__ = __add__ = __radd__ = __or__
	
	def __ior__(self, other):
		return set.__ior__(self, as_command_set(other))
	
	__iadd__ = __ior__
	
	def __sub__(self, other):
		return as_command_set(set.__sub__(self, as_command_set(other)))
	
	def __rsub__(self, other):
		return as_command_set(other) - self

	def __isub__(self, other):
		return as_command_set(set.__isub__(self, as_command_set(other)))
	
#-------------------------------------------------------------------------------

def as_command_set(x):
	if not isinstance(x, CommandSet):
		if isinstance(x, basestring):
			x = [x]
		x = CommandSet(x)
	return x

def filter_menu_items(items, include):
	result = []
	sep = False
	for item in items:
		if item == "-":
			sep = True
		elif item[1] in include:
			if sep:
				result.append("-")
				sep = False
			result.append(item)
	return result

def build_menus(spec_list, substitutions = {}, include = None, exclude = None):
	if include is None:
		include = sum(default_includes)
	include = include + sum(always_include)
	if exclude is not None:
		include = include - exclude
	menus = []
	for title, items, special in spec_list:
		items = filter_menu_items(items, include)
		if items:
			menus.append(Menu(title, items, special = special, substitutions = substitutions))
	return MenuList(menus)

#-------------------------------------------------------------------------------

fundamental_cmds = CommandSet(['quit_cmd'])
help_cmds = CommandSet(['about_cmd', 'help_cmd'])
pref_cmds = CommandSet(['preferences_cmd'])
file_cmds = CommandSet(['new_cmd', 'open_cmd', 'close_cmd', 'save_cmd', 'save_as_cmd', 'revert_cmd'])
print_cmds = CommandSet(['page_setup_cmd', 'print_cmd'])
edit_cmds = CommandSet(['undo_cmd', 'redo_cmd', 'cut_cmd', 'copy_cmd', 'paste_cmd', 'clear_cmd', 'select_all_cmd'])

always_include = [fundamental_cmds, edit_cmds]
default_includes = [help_cmds, pref_cmds, file_cmds, print_cmds]

#-------------------------------------------------------------------------------

if __name__ == "__main__":
	s1 = CommandSet('a')
	print "s1 =", s1
	s2 = CommandSet(['a', 'b'])
	print "s2 =", s2
	s3 = s2 + 'c'
	print "s3 =", s3
	s4 = 'd' + s3
	print "s4 =", s4
	s5 = s4 - 'b'
	print "s5 =", s5
	s6 = ['a', 'b', 'c', 'd', 'e', 'f'] - s5
	print "s6 =", s6
