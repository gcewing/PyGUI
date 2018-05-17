#
#		Python GUI - Menus - Gtk version
#

import gtk
from gtk import gdk
from GUI import export
from GUI.Globals import application
from GUI.GMenus import Menu as GMenu, MenuItem

def _report_accel_changed_(*args):
	print "Menus: accel_changed:", args

class Menu(GMenu):

	def __init__(self, title, items, **kwds):
		GMenu.__init__(self, title, items, **kwds)
		self._gtk_menu = gtk.Menu()
		self._gtk_accel_group = gtk.AccelGroup()
		#self._gtk_accel_group.connect('accel_changed', _report_accel_changed_) ###

	def _clear_platform_menu(self):
		gtk_menu = self._gtk_menu
		for gtk_item in gtk_menu.get_children():
			gtk_item.destroy()

	def _add_separator_to_platform_menu(self):
		gtk_item = gtk.MenuItem()
		gtk_item.set_sensitive(0)
		gtk_separator = gtk.HSeparator()
		gtk_item.add(gtk_separator)
		self._gtk_add_item(gtk_item)
	
	def _gtk_add_item(self, gtk_item):
		gtk_item.show_all()
		self._gtk_menu.append(gtk_item)

	def _add_item_to_platform_menu(self, item, name, command = None, index = None):
		checked = item.checked
		if checked is None:
			gtk_item = gtk.MenuItem(name)
		else:
			gtk_item = gtk.CheckMenuItem(name)
		self._gtk_add_item(gtk_item)
		if not item.enabled:
			gtk_item.set_sensitive(0)
		if checked:
			gtk_item.set_active(1)
		if command:
			app = application()
			if index is not None:
				action = lambda widget: app.dispatch(command, index)
			else:
				action = lambda widget: app.dispatch(command)
			gtk_item.connect('activate', action)
		key = item._key
		if key:
			gtk_modifiers = gdk.CONTROL_MASK
			if item._shift:
				gtk_modifiers |= gdk.SHIFT_MASK
			if item._option:
				gtk_modifiers |= gdk.MOD1_MASK
			gtk_item.add_accelerator('activate', self._gtk_accel_group,
				ord(key), gtk_modifiers, gtk.ACCEL_VISIBLE)

export(Menu)
