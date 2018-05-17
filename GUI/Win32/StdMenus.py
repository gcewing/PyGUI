#--------------------------------------------------------------------
#
#   PyGUI - Menus - Win32
#
#--------------------------------------------------------------------

from GUI.GStdMenus import build_menus, \
	fundamental_cmds, help_cmds, pref_cmds, file_cmds, print_cmds, edit_cmds

_file_menu_items = [
	("New/N",      'new_cmd'),
	("Open.../O",  'open_cmd'),
	("Close/W",    'close_cmd'),
	"-",
	("Save/S",     'save_cmd'),
	("Save As...", 'save_as_cmd'),
	("Revert",     'revert_cmd'),
	"-",
	("Page Setup...", 'page_setup_cmd'),
	("Print.../P",    'print_cmd'),
	"-",
	("Exit/Q",   'quit_cmd'),
]

_edit_menu_items = [
	("Undo/Z",       'undo_cmd'),
	("Redo/^Z",      'redo_cmd'),
	"-",
	("Cut/X",        'cut_cmd'),
	("Copy/C",       'copy_cmd'),
	("Paste/V",      'paste_cmd'),
	("Clear",        'clear_cmd'),
	"-",
	("Select All/A", 'select_all_cmd'),
	"-",
	("Preferences...", 'preferences_cmd'),
]

_help_menu_items = [
	("About <app>",    'about_cmd'),
]

#------------------------------------------------------------------------------

def basic_menus(substitutions = {}, include = None, exclude = None):
	return build_menus([
		("File", _file_menu_items, False),
		("Edit", _edit_menu_items, False),
		("Help", _help_menu_items, True),
	],
	substitutions = substitutions,
	include = include,
	exclude = exclude)
