#
#		Python GUI - Standard Menus - PyObjC
#

from GUI.GStdMenus import build_menus, \
	fundamental_cmds, help_cmds, pref_cmds, file_cmds, print_cmds, edit_cmds

fundamental_cmds += ['hide_app_cmd', 'hide_other_apps_cmd', 'show_all_apps_cmd']

_appl_menu_items = [
	("About <app>",    'about_cmd'),
	"-",
	("Preferences...", 'preferences_cmd'),
	"-",
	("Hide <app>/H",   'hide_app_cmd'),
	("Hide Others",    'hide_other_apps_cmd'),
	("Show All",       'show_all_apps_cmd'),
	"-",
	("Quit <app>/Q",   'quit_cmd'),
]

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
]

_edit_menu_items = [
	("Undo/Z",       'undo_cmd'),
	("Redo/^Z",      'redo_cmd'),
	"-",
	("Cut/X",        'cut_cmd'),
	("Copy/C",       'copy_cmd'),
	("Paste/V",      'paste_cmd'),
	("Delete",       'clear_cmd'),
	"-",
	("Select All/A", 'select_all_cmd'),
]

_help_menu_items = [
	("Help",         'help_cmd'),
]

#------------------------------------------------------------------------------

def basic_menus(substitutions = {}, include = None, exclude = None):
	return build_menus([
		("@",    _appl_menu_items, False),
		("File", _file_menu_items, False),
		("Edit", _edit_menu_items, False),
		("Help", _help_menu_items, True),
	],
	substitutions = substitutions,
	include = include,
	exclude = exclude)
