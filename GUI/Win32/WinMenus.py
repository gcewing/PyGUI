#--------------------------------------------------------------------
#
#   PyGUI - Menu utilities - Win32
#
#--------------------------------------------------------------------

from weakref import WeakKeyDictionary, WeakValueDictionary
import win32con as wc, win32ui as ui
from GUI import application

win_command_map = {}
win_command_list = []

def win_command_to_id(name, index = None):
	if index is not None:
		key = (name, index)
	else:
		key = name
	id = win_command_map.get(key)
	if not id:
		id = len(win_command_list) + 1
		win_command_map[key] = id
		win_command_list.append(key)
		application()._win_app.HookCommandUpdate(win_command_update, id)
	return id

def win_command_update(cmd):
	win_menu = cmd.m_pMenu
	if win_menu:
		menu = win_get_menu_for_hmenu(win_menu.GetHandle())
		if menu:
			item = menu._get_flat_item(cmd.m_nIndex)
			cmd.Enable(item.enabled)
			cmd.SetCheck(bool(item.checked))

def win_id_to_command(id):
	if 1 <= id <= len(win_command_list):
		return win_command_list[id - 1]

win_hmenu_to_menubar = WeakValueDictionary()

def win_get_menu_for_hmenu(hmenu):
	menubar = win_hmenu_to_menubar.get(hmenu)
	if menubar:
		return menubar.hmenu_to_menu.get(hmenu)

#--------------------------------------------------------------------

class MenuBar(object):
	#  Wrapper around a PyCMenu
	
	def __init__(self):
		self.win_menu = ui.CreateMenu()
		self.hmenu_to_menu = {}
	
	def append_menu(self, menu):
		win_menu = menu._win_create_menu()
		hmenu = win_menu.Detach()
		self.win_menu.AppendMenu(wc.MF_POPUP | wc.MF_STRING, hmenu, menu.title)
		win_hmenu_to_menubar[hmenu] = self
		self.hmenu_to_menu[hmenu] = menu
	
